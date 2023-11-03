SELECT
id as old_ownership_id,
user_id as old_user_id,
limit_id as old_limit_id,
created_at,
updated_at,
'1980-01-01 00:00:00.00000' ceased_at
FROM `RubyDB`.limit_ownerships;

INSERT INTO about.users (
old_limit_id,
SELECT
id as old_user_id,
login as old_login,
email as old_email
FROM RubyDB.users ;

INSERT INTO data.limits (
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
date_of_run_end, `year`
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
created_at, updated_at, creator_id, experiment, rating,
date_of_announcement, public, official, date_official,
greatest_hit, date_of_run_start,
date_of_run_end, `year`
FROM RubyDB.limits ;
