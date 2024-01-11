##echo 'This is a test' > init_new.sql
##echo ${FIRST_NAME} > init_new.sql

echo "CREATE USER '${MARIADB_USERNAME}'@'localhost' IDENTIFIED BY '${MARIADB_PASSWORD}';" > ../backup_db/init.sql

##echo "CREATE USER '${MARIADB_USERNAME}'@'127.0.0.1' IDENTIFIED BY '${MARIADB_PASSWORD}';" > ../backup_db/init.sql

echo "CREATE DATABASE backup;" >> ../backup_db/init.sql

echo "GRANT ALL PRIVILEGES ON *.* TO '${MARIADB_USERNAME}'@'localhost' WITH GRANT OPTION;" >> ../backup_db/init.sql

##echo "GRANT ALL PRIVILEGES ON *.* TO '${MARIADB_USERNAME}'@'127.0.0.1' WITH GRANT OPTION;" >> ../backup_db/init.sql

echo "ALTER USER '${MARIADB_USERNAME}'@'%' IDENTIFIED BY '${MARIADB_PASSWORD}';" >> ../backup_db/init.sql

echo "GRANT ALL PRIVILEGES ON *.* TO '${MARIADB_USERNAME}'@'%' WITH GRANT OPTION;" >> ../backup_db/init.sql

## This is required when using Dockerfile
