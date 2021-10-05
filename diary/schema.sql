DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS diary_entries;
DROP TABLE IF EXISTS diaries;
DROP TABLE IF EXISTS contributors;

CREATE TABLE users (
    username TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    password TEXT NOT NULL,
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
    contributor TEXT NOT NULL,
    diary_id INTEGER NOT NULL,
    primary_contributor BOOLEAN NOT NULL,
    FOREIGN KEY(contributor) REFERENCES users(username),
    FOREIGN KEY(diary_id) REFERENCES diaries(id),
    PRIMARY KEY (contributor, diary_id)
);