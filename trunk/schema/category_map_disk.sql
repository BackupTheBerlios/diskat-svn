CREATE TABLE category_map_disk(
  id INTEGER PRIMARY KEY,
  cat_id INT NOT NULL,
  obj_id INT NOT NULL,
  tstamp CHAR(14) NOT NULL
);

CREATE INDEX cmd_catid ON category_map(cat_id);
CREATE INDEX cmd_objid ON category_map(obj_id);
