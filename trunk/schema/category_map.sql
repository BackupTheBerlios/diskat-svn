CREATE TABLE category_map(
  id INTEGER PRIMARY KEY,
  cat_id INT NOT NULL,
  obj_id INT NOT NULL,
  tstamp CHAR(14) NOT NULL,
  value VARCHAR(256) NOT NULL
);

CREATE INDEX cm_catid ON category_map(cat_id);
CREATE INDEX cm_objid ON category_map(obj_id);
