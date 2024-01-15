## Run the following Shell Scripts

### 0_

    source 0_setenv+copyenvfiles.sh

### 1_

    source 1_create_pod.sh

### 2_

    source 2_make_redis.sh

### 3_

    3_make_mariadb.sh

## Run SQL Procedure Move Data

      during container creation it was not possible to create and populate a different schema with a script
      the data from the original DMTOOLS loads into the data schema and this procedure moves the data
      across into RubyDB. Later the data is migrated into the new tables within data schema.

      { CALL `data`.move_data() }

## Run Following Shell Scripts

    the fastapi containers follow a pretty standard recipe

    there is some inconsistency when returning list of classes. Some are class based returns and some are simple list of dicts.

    Relationship were attempted to create nested classes being returned. These just did not work?

### 4_

    the fastapi_data container provides CRUD access to all data
    there are both internal and external apis 

    source 4_make_fastapi_data.sh

### 5_

    the fastapi_about container is an internal container only as it allows
    the management of users and api keys.
    
    5_make_fastapi_about.sh

## Prime data tables

    the way fastapi works is that it takes over a whole database and monitors changes to tables
    the priming creates the brand new tables and establishes a baseline.

    If any changes are made to the tables, update_migration.sh should be run.

      cd ..
      cd fastapi_data
      
      source prime_db_migration_dev.sh

## Prime about tables

      cd ..
      cd fastapi_about
      
      source prime_db_migration_dev.sh

## Migrate the Ruby Data to Data Tables

    { CALL `data`.migrate_data() }

## Populate Data for Dropdown Filter Controls

    { CALL `data`.update_dropdownpair() }

## Create the Frontend Application

    cd ..
    cd create
    source 6_make_application.sh

## Create the NGINX Container

  This is the only container that needs to be run as supervisor as port 443 is a privileged port

    cd ..
    cd networking

    sudo su

    source clean+create443dev.sh

    exit

## Visit Site to check working

    https://dev1.dmtool.info/

    select login

    enter google user id e.g. email address

    enter google password

    enter registered mobile phone number

    receive and enter Google verification code

    start exploring

## Data Ownership is created as data is uploaded by user

### /* findout your user id */

        SELECT authlib_id, authlib_provider, email, old_user_id, old_login, old_email, created_at, updated_at, ceased_at, id
        FROM about.`user`;

### /* you need to upload data to have some data to select to plot */

        SELECT data_values, old_limit_id, spin_dependency, result_type, measurement_type, nomhash, x_units, y_units, x_rescale, y_rescale, default_color, default_style, data_label, file_name, data_comment, data_reference, created_at, updated_at, archived_at, creator_id, experiment, rating, date_of_announcement, public, official, date_official, greatest_hit, date_of_run_start, date_of_run_end, `year`, id
        FROM `data`.`limit`;

### /* we will allocate some data to a user */


        select 1 as user_id, id as limit_id , now() as created_at, now() as update_at, '1980-01-01 12:00:00' as archived_at FROM `data`.`limit`;
        
        SELECT old_ownership_id, user_id, limit_id, old_user_id, old_limit_id, created_at, updated_at, archived_at, id
        FROM `data`.limit_ownership;
        
        /*
        INSERT INTO tbl_temp2 (fld_id)
          SELECT tbl_temp1.fld_order_id
          FROM tbl_temp1 WHERE tbl_temp1.fld_order_id > 100;
        */
        
        INSERT INTO `data`.limit_ownership (user_id, limit_id, created_at, updated_at, archived_at )
select 1 as user_id, id as limit_id , now() as created_at, now() as updated_at, '1980-01-01 12:00:00' as archived_at FROM `data`.`limit`;
   








