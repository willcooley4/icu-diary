PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS diary_entry;
DROP TABLE IF EXISTS diary;
DROP TABLE IF EXISTS contributors;

CREATE TABLE users (
    username TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    password TEXT NOT NULL,
    profile_pic TEXT NOT NULL
);

CREATE TABLE diary_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    contents TEXT NOT NULL,
    media TEXT,
    author TEXT NOT NULL,
    diary_id INTEGER NOT NULL
    FOREIGN KEY (author) REFERENCES users (username),
    FOREIGN KEY (diary_id) REFERENCES diaries (id)
);

CREATE TABLE diaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    patient TEXT NOT NULL
);

CREATE TABLE contributors (
    contributor TEXT NOT NULL,
    diary_id TEXT NOT NULL,
    primary_contributor BOOLEAN NOT NULL,
    FOREIGN KEY (contributor) REFERENCES users (username),
    FOREIGN KEY (diary_id) REFERENCES diaries (id),
    PRIMARY KEY (contributor, diary_id)
);