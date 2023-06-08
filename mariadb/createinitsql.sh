##echo 'This is a test' > init_new.sql
##echo ${FIRST_NAME} > init_new.sql

echo "CREATE USER '${MARIADB_USERNAME}'@'localhost' IDENTIFIED BY '${MARIADB_PASSWORD}';" > ../mariadb/init.sql

echo "CREATE DATABASE data;" >> ../mariadb/init.sql

echo "GRANT ALL PRIVILEGES ON *.* TO '${MARIADB_USERNAME}'@'localhost' WITH GRANT OPTION;" >> ../mariadb/init.sql

echo "ALTER USER '${MARIADB_USERNAME}'@'%' IDENTIFIED BY '${MARIADB_PASSWORD}';" >> ../mariadb/init.sql

echo "GRANT ALL PRIVILEGES ON *.* TO '${MARIADB_USERNAME}'@'%' WITH GRANT OPTION;" >> ../mariadb/init.sql

## This is required when using Dockerfile
