##echo 'This is a test' > init_new.sql
##echo ${FIRST_NAME} > init_new.sql

echo "CREATE USER '${PYTHONUSER}'@'localhost' IDENTIFIED BY '${PYTHONUSERPASSWORD}';" > ../mariadb/init.sql

echo "CREATE DATABASE data;" >> ../mariadb/init.sql

echo "GRANT ALL PRIVILEGES ON *.* TO '${PYTHONUSER}'@'localhost' WITH GRANT OPTION;" >> ../mariadb/init.sql

echo "ALTER USER '${PYTHONUSER}'@'%' IDENTIFIED BY '${PYTHONUSERPASSWORD}';" >> ../mariadb/init.sql

echo "GRANT ALL PRIVILEGES ON *.* TO '${PYTHONUSER}'@'%' WITH GRANT OPTION;" >> ../mariadb/init.sql

## This is required when using Dockerfile
