BEGIN TRANSACTION;

-- ALTER TABLE directory RENAME TO directory_t;

CREATE TABLE category_t(
  id INTEGER PRIMARY KEY,
  type INT NOT NULL,
  name VARCHAR(128) NOT NULL
);

INSERT INTO category_t SELECT * FROM category;
DROP TABLE category;

CREATE TABLE category(
  id INTEGER PRIMARY KEY,
  type INT NOT NULL,
  value_type INT NOT NULL DEFAULT 1,
  name VARCHAR(128) NOT NULL
);

INSERT INTO category(id, type, value_type, name)
SELECT id, type, 1, name
FROM category_t;

DROP TABLE category_t;

COMMIT;
