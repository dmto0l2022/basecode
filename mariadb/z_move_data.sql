DELIMITER //

CREATE DEFINER='{$MARIADB_USERNAME}'@'%' PROCEDURE data.move_data()
BEGIN

/* RubyDB.experiments; */
CREATE TABLE RubyDB.experiments
AS
SELECT * from data.experiments;

DROP TABLE data.experiments;

/* RubyDB.limit_displays; */

CREATE TABLE RubyDB.limit_displays
AS
SELECT * from data.limit_displays;

DROP TABLE data.limit_displays;

/* RubyDB.limit_ownerships; */

CREATE TABLE RubyDB.limit_ownerships
AS
SELECT * from data.limit_ownerships;

DROP TABLE data.limit_ownerships;

/* RubyDB.plot_ownerships; */

CREATE TABLE RubyDB.plot_ownerships
AS
SELECT * from data.plot_ownerships;

DROP TABLE data.plot_ownerships;

/* RubyDB.plots; */

CREATE TABLE RubyDB.plots
AS
SELECT * from data.plots;

DROP TABLE data.plots;

/* RubyDB.limits; */

CREATE TABLE RubyDB.limits
AS
SELECT * from data.limits;

DROP TABLE data.limits;

/* RubyDB.users; */

CREATE TABLE RubyDB.users
AS
SELECT * from data.users;

DROP TABLE data.users;

DROP TABLE data.schema_migrations;

DROP TABLE data.simple_captcha_data;

END;
//
DELIMITER ;
