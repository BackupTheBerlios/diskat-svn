CREATE TABLE disk(
  id INTEGER PRIMARY KEY,
  last_update INTEGER NOT NULL,
  tag VARCHAR(16) NOT NULL,
  -- Root (mount point) of this disk when it was captured
  root VARCHAR(1024) NOT NULL,
  location INT NOT NULL DEFAULT 2,
  temp_location INT NOT NULL DEFAULT 1,
  label VARCHAR(64) NOT NULL,
  -- OS Unique disk ID
  serial VARCHAR(64) NOT NULL,
  title VARCHAR(64) NOT NULL,
  -- Number of ordinary files
  n_files INT NOT NULL DEFAULT 0,
  -- Number of directories
  n_dirs INT NOT NULL DEFAULT 0,
  -- Number of ordinary files in archives
  n_a_files INT NOT NULL DEFAULT 0,
  -- Number of directories in archives
  n_a_dirs INT NOT NULL DEFAULT 0,
  -- Number of archives
  n_arcs INT NOT NULL DEFAULT 0,
  description VARCHAR(16384) NOT NULL DEFAULT '',
  desc_type INT NOT NULL DEFAULT 0,
  notes VARCHAR(16384) NOT NULL DEFAULT ''
);

CREATE UNIQUE INDEX disk_tag ON disk(tag);
