for line in $(mysql -u $MARIADB_USERNAME -p $MARIADB_PASSWORD -AN -e "show tables from data");
do
timestamp=$(date +%s)
filename=$line
fileextension='.sql'
folderpath = '/data/containers/data/backups/'
fullfilepath="${folderpath} ${filename} $(timestamp) $(fileextension)"
echo "${fullfilepath}"
mysqldump -u $MARIADB_USERNAME -p $MARIADB_PASSWORD data $line > $fullfilepath ; 
done
