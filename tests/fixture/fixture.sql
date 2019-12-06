CREATE TABLE IF NOT EXISTS file (
    id SERIAL,
    name TEXT NOT NULL,

    PRIMARY KEY(id)
);

CREATE UNIQUE INDEX IF NOT EXISTS uniq_file_name ON file(name);

CREATE TABLE IF NOT EXISTS dataset (
    id SERIAL,
    dataset jsonb NOT NULL,

    PRIMARY KEY(id)
);

-- we assume the files were already uploaded
INSERT INTO file (
    id,
    name
)
VALUES (1, 'test_file_first_csv'), (2, 'test_file_second_csv');