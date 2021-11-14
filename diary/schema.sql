DROP TABLE IF EXISTS diary_entries;
DROP TABLE IF EXISTS contributors;
DROP TABLE IF EXISTS diaries;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    username TEXT PRIMARY KEY,
    user_type TEXT NOT NULL,
    full_name TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    profile_pic TEXT NOT NULL
);

CREATE TABLE diaries (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    patient TEXT NOT NULL
);

CREATE TABLE diary_entries (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    contents TEXT NOT NULL,
    media TEXT,
    author TEXT NOT NULL,
    diary_id INTEGER NOT NULL,
    FOREIGN KEY(author) REFERENCES users(username),
    FOREIGN KEY(diary_id) REFERENCES diaries(id)
);

CREATE TABLE contributors (
    contributor TEXT PRIMARY KEY,
    diary_id INTEGER NOT NULL,
    approved BOOLEAN NOT NULL,
    primary_contributor BOOLEAN NOT NULL,
    FOREIGN KEY(contributor) REFERENCES users(username),
    FOREIGN KEY(diary_id) REFERENCES diaries(id)
);
