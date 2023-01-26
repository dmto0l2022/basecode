#cp ./.env ../
# remember to paste the .env file into aa_build before running this

cp ./.env ../mariadb/.env
cp ./.env ../flask_crud_api/app/.env
cp ./.env ../flask_dash_frontend/app/.env
## set the variables for the mariadb 
source ../mariadb/setenv.sh
source ../mariadb/createinitsql.sh

