BEGIN TRANSACTION;

-- ALTER TABLE directory RENAME TO directory_t;

CREATE TABLE directory_t(
  id INTEGER PRIMARY KEY,
  snapshot INT NOT NULL,
  no INT NOT NULL DEFAULT 0,
  parent INT NOT NULL,
  name VARCHAR(512) NOT NULL,
  extension VARCHAR(16) NOT NULL,
  size INT NOT NULL DEFAULT 0,
  is_dir INT NOT NULL DEFAULT 0,
  arc_status INT NOT NULL DEFAULT 0,
  better_name VARCHAR(512) NOT NULL DEFAULT '',
  description VARCHAR(16384) NOT NULL DEFAULT '',
  notes VARCHAR(16384) NOT NULL DEFAULT ''
);
INSERT INTO directory_t SELECT * FROM directory;
DROP TABLE directory;

CREATE TABLE directory(
  id INTEGER PRIMARY KEY,
  snapshot INT NOT NULL,
  no INT NOT NULL DEFAULT 0,
  parent INT NOT NULL,
  name VARCHAR(512) NOT NULL,
  extension VARCHAR(16) NOT NULL,
  size INT NOT NULL DEFAULT 0,
  is_dir INT NOT NULL DEFAULT 0,
  arc_status INT NOT NULL DEFAULT 0,
  mdate VARCHAR(14) NOT NULL DEFAULT '00000000000000',
  better_name VARCHAR(512) NOT NULL DEFAULT '',
  description VARCHAR(16384) NOT NULL DEFAULT '',
  notes VARCHAR(16384) NOT NULL DEFAULT ''
);

CREATE INDEX dir_snapshot ON directory(snapshot);
CREATE INDEX dir_parent ON directory(parent);

INSERT INTO directory(id, snapshot, no, parent, name, extension, size, is_dir, arc_status, better_name, description, notes)
SELECT *
FROM directory_t;
DROP TABLE directory_t;

COMMIT;
