CREATE TABLE location(
  id INTEGER PRIMARY KEY,
  name VARCHAR(64) NOT NULL,
  description VARCHAR(512) NOT NULL
);

INSERT INTO location(id, name, description)
VALUES (1, '<none>', 'None location');
INSERT INTO location(id, name, description)
VALUES (2, '<unspecified>', 'Unspecified location');
