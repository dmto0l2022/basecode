DELIMITER //

/* "CREATE USER '{$MYSQL_USER}' IDENTIFIED BY '${MYSQL_USER_PASSWORD}'" */
	
CREATE DEFINER='{$MARIADB_USERNAME}'@'%' PROCEDURE data.migrate_data()
BEGIN
    
INSERT INTO data.experiment(old_experiment_id,name,created_at,updated_at,archived_at)
SELECT id as old_experiment_id, name,
'1980-01-01 00:00.00.00000' created_at,
'1980-01-01 00:00.00.00000' updated_at,
'1980-01-01 00:00.00.00000' archived_at
FROM RubyDB.experiments;

INSERT INTO data.limit_display(
	old_limit_display_id,
  	old_limit_id, old_plot_id, old_color,
  	old_style,
  	created_at,
  	updated_at,
  	archived_at)
SELECT
id as old_limit_display_id,
limit_id as old_limit_id,
plot_id as old_plot_id,
color as old_color,
`style` as old_style,
created_at,
updated_at,
'1980-01-01 00:00.00.00000' ceased_at
FROM RubyDB.limit_displays;

INSERT INTO data.limit_ownership(
old_ownership_id,
old_user_id,
old_limit_id,
created_at,
updated_at,
archived_at)
SELECT
id as old_ownership_id,
user_id as old_user_id,
limit_id as old_limit_id,
created_at,
updated_at,
'1980-01-01 00:00.00.00000' archived_at
FROM RubyDB.limit_ownerships;

INSERT INTO data.plot_ownership(old_plot_ownership_id, old_user_id, old_plot_id, created_at, updated_at, archived_at)
SELECT
id as old_plot_ownership_id,
user_id as old_user_id,
plot_id as old_plot_id,
created_at, 
updated_at,
'1980-01-01 00:00.00.00000' archived_at
FROM RubyDB.plot_ownerships;

INSERT INTO data.plot(old_plot_id, name,
x_min,x_max,y_min,y_max,x_units,y_units,old_user_id,
created_at,updated_at,no_id, archived_at)
SELECT 
id as old_plot_id,
name,
x_min,
x_max,
y_min,
y_max,
x_units,
y_units,
user_id as old_user_id,
created_at,
updated_at,
no_id,
'1980-01-01 00:00.00.00000' archived_at
FROM RubyDB.plots;

/*
INSERT INTO about.user (
old_user_id,
old_login,
old_email,
created_at,
updated_at,
ceased_at)
SELECT
id as old_user_id,
login as old_login,
email as old_email,
'1980-01-01 00:00.00.00000' created_at,
'1980-01-01 00:00.00.00000' updated_at,
'1980-01-01 00:00.00.00000' ceased_at
FROM RubyDB.users ;
*/

INSERT IGNORE INTO data.limit (
old_limit_id,
spin_dependency,
result_type,
measurement_type,
nomhash, x_units, y_units, x_rescale, y_rescale, default_color,
default_style, data_values,
data_label,
file_name,
data_comment,data_reference,
created_at, updated_at, creator_id, experiment, rating,
date_of_announcement, public, official, date_official,
greatest_hit, date_of_run_start,
date_of_run_end, `year`,
archived_at
)
SELECT
id as old_limit_id,
spin_dependency,
result_type,
measurement_type,
nomhash, x_units, y_units, x_rescale, y_rescale, default_color,
default_style, data_values,
data_label,
file_name,
data_comment,data_reference,
created_at,
updated_at,
creator_id,
experiment,rating,
date_of_announcement,
public,
official,
date_official,
greatest_hit,
date_of_run_start,
date_of_run_end,
'year',
'1980-01-01 00:00.00.00000' archived_at
FROM RubyDB.limits;
	
END;
//
DELIMITER ;
