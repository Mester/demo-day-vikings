PRAGMA foreign_keys = ON;

DROP TABLE if exists songs;
CREATE TABLE songs (
    id INTEGER PRIMARY KEY autoincrement,
    genre TEXT,
    title TEXT,
    artist TEXT,
    yr INTEGER,
    url TEXT,
    score INTEGER,
    posted_utc REAL,
    thumbnail TEXT
    );
