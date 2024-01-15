DELIMITER //

CREATE DEFINER=`pythonuser`@`%` PROCEDURE `data`.`backup_tables`()
BEGIN	
	DECLARE done INT DEFAULT FALSE;
	DECLARE x, y INT;
	DECLARE tname CHAR(255);
	DECLARE cur1 CURSOR FOR SELECT i FROM data.c1;
	DECLARE cur2 CURSOR FOR SELECT i FROM data.c2;
	DECLARE TablesCursor CURSOR FOR	SELECT TABLE_NAME FROM information_schema.tables a where TABLE_SCHEMA = 'data';
		
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;	

	/*set @tname := 'table_name';*/
	set @ts:= cast(current_timestamp +0 as char);
	set @backup_folder:= '/data/backups/';
	set @data_base := 'data';
	set @dot := '.' ;
	set @filename:= 'filename_1';
	set @fileextension := '.txt';
	set @fullname = concat(@backup_folder, @ts, @filename, @fileextension );
	
	##select @fullname;
	
	/*
	OPEN cur1;
	OPEN cur2;
	
	read_loop: LOOP
		FETCH cur1 INTO x;
		FETCH cur2 INTO y;
		select @fullname;
	END LOOP;
	
	CLOSE cur1;
	CLOSE cur2;
	*/
	OPEN TablesCursor;

	read_loop: LOOP
		FETCH TablesCursor INTO tname;
		#set @quoted_table = QUOTE(tname);
		
		set @full_table_name = concat(@data_base, @dot, tname);
		set @full_filename = concat(@backup_folder, @ts, tname, @fileextension );
		
		/*
		concat('SELECT * from ', @full_table_name ,' INTO OUTFILE ', @full_filename, 
		FIELDS TERMINATED BY \',' LINES TERMINATED BY \'\n\';)
		*/
	
		/*
		 SELECT id from data.limit
		  INTO OUTFILE '/data/containers/data/backups/test.txt'
		  FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
		  LINES TERMINATED BY '\n';
		 */
	
		#SET @sql_text1 = concat('SELECT MIN(',@keyField,') INTO @a FROM ',@table_name);
		SET @sql_text1 = concat('SELECT * from ', @full_table_name ,' INTO OUTFILE \'', @full_filename,
		'\' FIELDS TERMINATED BY \',\' OPTIONALLY ENCLOSED BY \'\"\' LINES TERMINATED BY \'\n\';');
		
		PREPARE stmt1 FROM @sql_text1;
	    EXECUTE stmt1;
	   
		/*
		SET @tableName = 'data.c1';
		SET @query = CONCAT('SELECT * FROM ', @full_table_name);
		PREPARE stmt FROM @query;
		EXECUTE stmt;
		*/
	
	END LOOP;
	
	CLOSE TablesCursor;

END;

//
DELIMITER ;
