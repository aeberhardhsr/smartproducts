-- SQL Statements to Create the Database to store the information from the smart shopping cart
-- Table records: the predicted id from the image is stored in this table
-- Table product: all information from the product is stored in this table
-- the tables are linked with a FOREIGN KEY relation

/*
 * CREATE USER
 */
DROP USER IF EXISTS spuser;
CREATE USER 'spuser'@'localhost' IDENTIFIED BY 'spuser';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, FILE, INDEX, ALTER, CREATE TEMPORARY TABLES, CREATE VIEW, EVENT, TRIGGER, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, EXECUTE ON *.* TO 'spuser'@'localhost' REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;

/*
 * CREATE DATABASE
 */
DROP DATABASE IF EXISTS smartproducts;
CREATE DATABASE smartproducts;
USE smartproducts;

/*
 * CREATE TABLES
 */
CREATE TABLE records (
  rec_id INTEGER AUTO_INCREMENT PRIMARY KEY,
  rec_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  p_id INTEGER NOT NULL
);

CREATE TABLE products (
  p_id INTEGER PRIMARY KEY,
  p_name VARCHAR(50) UNIQUE,
  p_weight FLOAT(30),
  p_price FLOAT(30)
);

/*
 * ADD CONSTRAINTS
 */
ALTER TABLE records
ADD CONSTRAINT fk_products_records
	FOREIGN KEY (p_id) REFERENCES products(p_id)
;

/*
 * ADD VALUES TO THE TABLE products
 */
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (0,'bio mclassic erbsen fein',150, 7.50);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (1,'primella wattestaebchen',160, 6.50);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (2,'bio mclassic erbsen fein (dose)',170, 8.50);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (3,'mclassic gruene spargelspitzen',180, 4.50);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (4,'tea time kamille',190, 2.50);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (5,'zitronensaft',140, 3.05);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (6,'bio mclassic apfelmus',130, 7.25);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (7,'kelloggs variety',230, 6.75);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (8,'aproz classic (flasche)',450, 2.35);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (9,'zweifel chips nature',350, 4.35);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (10,'tea time pfefferminze',100, 2.45);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (11,'bio mclassic maiskoerner',250, 3.25);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (12,'bio mclassic apfelmus (dose)',235, 3.25);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (13,'mbudget kraeuter shampoo',450, 6.85);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (14,'bio mclassic maiskoerner (dose)',265, 3.55);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (15,'aproz medium (flasche)',450, 2.45);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (16,'aproz classic',550, 2.45);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (17,'bellena festseife',195, 3.75);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (18,'aproz medium',550, 2.55);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (19,'mclassic weisse spargelspitzen',350, 4.75);
INSERT INTO products (p_id,p_name,p_weight, p_price) VALUES (20,'zweifel paprika',195, 3.65);