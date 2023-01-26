#cp ./.env ../
# remember to paste the .env file into create before running this

cp ./.env ../mariadb/.env
cp ./.env ../api/app/.env
cp ./.env ../frontend/app/.env
cp ./.env ../dashapps/app/.env
## set the variables for the mariadb 
source ../mariadb/setenv.sh
source ../mariadb/createinitsql.sh

