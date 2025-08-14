# Music Collection CLI (SQLite)

A simple, fully interactive command‑line app to manage users and their song collections using SQLite for persistence.
The original program logic is in `music_app.py` (ported from your submission).

## Features
- Create and switch users
- Add, update, delete songs
- View a user's collection
- Data persisted to `music.db` via SQLite

## Run locally (no Docker)
```bash
python3 music_app.py
```

## Docker
Build the image:
```bash
docker build -t music-collection-cli .
```

Run it (persisting your `music.db` to a local `data/` folder):
```bash
mkdir -p data
docker run --rm -it -v "$PWD/data:/data" music-collection-cli
```

- The app runs in interactive mode.
- The working directory inside the container is `/data`, so your `music.db` is saved under `./data/music.db` on your host.

## Project structure
```text
music-collection-cli/
├─ Dockerfile
├─ .dockerignore
├─ README.md
└─ music_app.py
```

## Notes
- This container uses the official `python:3.12-slim` base image.
- No third‑party packages are required (only Python standard library + SQLite3).
