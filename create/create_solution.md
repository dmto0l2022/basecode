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

    








