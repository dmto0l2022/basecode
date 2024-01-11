# remember to paste the .env file into create before running this

cp ./.env ../mariadb/.env
cp ./.env ../fastapi_data/app/.env
cp ./.env ../fastapi_about/app/.env
cp ./.env ../application/app/.env
cp ./.env ../application/app/baseapp/.env
cp ./.env ../backup_db/.env

## set the variables for the mariadb 
source ../mariadb/setenv.sh
source ../mariadb/createinitsql.sh
source ../backup_db/createinitsql.sh

