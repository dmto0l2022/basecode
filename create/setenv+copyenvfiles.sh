# remember to paste the .env file into create before running this

cp ./.env ../mariadb/.env
cp ./.env ../fastapi_alembic/app/.env
cp ./.env ../login/app/.env
cp ./.env ../login/app/baseapp/.env
## set the variables for the mariadb 
source ../mariadb/setenv.sh
source ../mariadb/createinitsql.sh

