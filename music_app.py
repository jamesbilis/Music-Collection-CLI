import sqlite3
#Greeting for the program.
def welcome_message():
    print("\nWelcome to the Music Collection Machine! To get started, please select an option from the menu below.")

#Initializes Database Containing User/User Info
def initialize_database():
    conn = sqlite3.connect("music.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
            )
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            artist TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

#Loads User Info from Database File
def load_users_from_db():
    conn = sqlite3.connect("music.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM users")
    user_rows = cursor.fetchall()

    for user_id, name in user_rows:
        user = User(name)
        users[name] = user

        cursor.execute("SELECT title, artist FROM songs WHERE user_id = ?", (user_id,))
        song_rows = cursor.fetchall()

        for title, artist in song_rows:
            user.collection[title] = artist

    conn.close()

#Creates User Class
class User:
    def __init__(self, name):
        self.name = name
        self.collection = {}

    def __str__(self):
        return self.name

users = {}
current_user = None

#Function to Add New User
def add_user():
    global current_user
    add_user = input("Please enter a new username: ")

    if add_user in users:
        print("User already exists.")
        current_user = users[add_user]
        return

    conn = sqlite3.connect("music.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (name) VALUES (?)", (add_user,))
        conn.commit()
        print(f"User '{add_user}' added to database.")
    except sqlite3.IntegrityError:
        print("Username already exists in database.")
        conn.close()
        return

    cursor.execute("SELECT id FROM users WHERE name = ?", (add_user,))
    user_id = cursor.fetchone()[0]
    conn.close()

    new_user = User(add_user)
    users[add_user] = new_user
    current_user = new_user
    print(f"User '{current_user}' has been added and set as current user.")

#Function to Change User
def change_user():
    global current_user
    if not users:
        print("No users are available. Please add a user.")
    else:
        print("Choose a user: ")
        user_list = list(users.values())
        for i, user in enumerate(user_list, 1):
            print(f"{i}) {user}")
        selection = input(">> Enter the number of the user: ")
        if selection.isdigit():
            index = int(selection) - 1
            if 0 <= index < len(user_list):
                current_user = user_list[index]
                print(f"Switched to user: {current_user}")
            else:
                print("Invalid number.")
        else:
            print("Please enter a valid number.")

#Function to Add New Song
def add_song():
    if current_user:
        title = input("Please enter a song title: ")
        artist = input(f"Great! The song title is '{title}'. Please enter the artist name: ")
        current_user.collection[title] = artist

        conn = sqlite3.connect("music.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE name = ?", (current_user.name,))
        user_id = cursor.fetchone()[0]

        cursor.execute("INSERT INTO songs (user_id, title, artist) VALUES (?, ?, ?)",
                       (user_id, title, artist))
        conn.commit()
        conn.close()

        print(f"The song: '{title}' by '{artist}' has been added to {current_user}'s music collection.")
    else:
        print("No user selected. Please add or change user first.")

#Function to View the Current User's Music Collection
def view_collection():
    if current_user:
        if current_user.collection:
            print(f"\n=== {current_user}'s Music Collection ===")
            for i, (title, artist) in enumerate(current_user.collection.items(), 1):
                print(f"{i}) {title} by {artist}")
        else:
            print(f"{current_user} has no songs in their collection.")
    else:
        print("No user selected.")

#Function to View a Song's Details
def view_song_details():
    if current_user:
        title = input("Please enter a song to look up: ")
        if title in current_user.collection:
            print(f" {title} is by {current_user.collection[title]}")
        else:
            print(f"{title} not found in {current_user}'s collection.")
    else:
        print("No user selected.")

#function to Update a Song's Details
def update_song_details():
    if current_user and current_user.collection:
        print(f"\n=== {current_user}'s Music Collection ===")
        songs = list(current_user.collection.items())
        for i, (title, artist) in enumerate(songs, 1):
            print(f"{i}) {title} by {artist}")
        selection = input(">> Enter the number of the song to update: ")
        if selection.isdigit():
            index = int(selection) - 1
            if 0 <= index < len(songs):
                old_title = songs[index][0]
                new_artist = input(f"Enter new artist for '{old_title}': ")
                current_user.collection[old_title] = new_artist

                # Updates in database
                conn = sqlite3.connect("music.db")
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE name = ?", (current_user.name,))
                user_id = cursor.fetchone()[0]

                cursor.execute("""
                    UPDATE songs
                    SET artist = ?
                    WHERE user_id = ? AND title = ?
                """, (new_artist, user_id, old_title))
                conn.commit()
                conn.close()

                print(f"Updated '{old_title}' to new artist: {new_artist}")
            else:
                print("Invalid number.")
        else:
            print("Please enter a valid number.")
    else:
        print("No songs available to update.")

#Function to Delete a Song from the Database
def delete_song():
    if current_user and current_user.collection:
        print(f"\n=== {current_user}'s Music Collection ===")
        songs = list(current_user.collection.items())
        for i, (title, artist) in enumerate(songs, 1):
            print(f"{i}) {title} by {artist}")
        selection = input(">> Enter the number of the song to delete: ")
        if selection.isdigit():
            index = int(selection) - 1
            if 0 <= index < len(songs):
                title_to_delete = songs[index][0]
                del current_user.collection[title_to_delete]

                # Delete from database
                conn = sqlite3.connect("music.db")
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE name = ?", (current_user.name,))
                user_id = cursor.fetchone()[0]

                cursor.execute("""
                    DELETE FROM songs
                    WHERE user_id = ? AND title = ?
                """, (user_id, title_to_delete))
                conn.commit()
                conn.close()

                print(f"Deleted '{title_to_delete}' from {current_user}'s music collection.")
            else:
                print("Invalid number.")
        else:
            print("Please enter a valid number.")
    else:
        print("No songs available to delete.")

#Functions being run to get program started
initialize_database()
load_users_from_db()
welcome_message()

#While loop to Display Menu and Handle User Responses. Links a choice to it's appropriate function.
while True:
    print("\n=== Menu ===")
    if current_user:
        print(f"=== Current User: {current_user} ===")
    print("1) Add User")
    print("2) Change User")
    print("3) Add Song")
    print("4) View Song Details")
    print("5) Update Song Details")
    print("6) Delete Song")
    print("7) View Music Collection")
    print("0) Exit")
    choice = input("\nWhat would you like to do? ")
    if choice == "1":
        add_user()
    elif choice == "2":
        change_user()
    elif choice == "3":
        add_song()
    elif choice == "4":
        view_song_details()
    elif choice == "5":
        update_song_details()
    elif choice == "6":
        delete_song()
    elif choice == "7":
        view_collection()
    elif choice == "0":
        print("\nAlright! See you next time!")
        break


