## Introduction

    The existing eps and png plots were extracted to the server.

    Best way to download them to a local drive was to zip them into a single file.
    The download them using Download File in the Google Console where you start and stop the server.

    I tried gdrive and rclone and both were challenging you you are working headless.

    The purpose is to find good plots to recreate and what limits/datasets all users should have access to
    
## Default Styles Discovered

    ##if result_type == 'Th' then fill else nofil
    ##if spin_dependency = 'SD' then dash
    ##if spin_dependency = 'SI' then line


## SQL Procedure used

      CREATE DEFINER=`pythonuser`@`%` PROCEDURE `data`.`extract_plots`()
      BEGIN	
      	DECLARE plot_id INT;
      	DECLARE PlotCursor CURSOR FOR SELECT id FROM RubyDB.plots a;
      		
      	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;	
      
      	
      	set @ts:= cast(current_timestamp +0 as char);      	
      	
      	OPEN PlotCursor;
      
      	read_loop: LOOP
      		FETCH PlotCursor INTO plot_id;	
      	
      		set @ts:= cast(current_timestamp +0 as char);
      
      		SET @sql_text1 = concat('SELECT plot_png FROM RubyDB.plots WHERE id=',plot_id,' INTO DUMPFILE \"/data/backups/', plot_id , '_plot_png_', @ts, '.png\";');
      		SET @sql_text2 = concat('SELECT legend_png FROM RubyDB.plots WHERE id=',plot_id,' INTO DUMPFILE \"/data/backups/', plot_id , '_legend_png_', @ts, '.png\";');
      		SET @sql_text3 = concat('SELECT plot_eps FROM RubyDB.plots WHERE id=',plot_id,' INTO DUMPFILE \"/data/backups/', plot_id , '_plot_eps_', @ts, '.eps\";');
      		SET @sql_text4 = concat('SELECT legend_eps FROM RubyDB.plots WHERE id=',plot_id,' INTO DUMPFILE \"/data/backups/', plot_id ,'_legend_eps_', @ts, '.eps\";');
      		
      		PREPARE stmt1 FROM @sql_text1;
      	    EXECUTE stmt1;
      	    
      	   	PREPARE stmt2 FROM @sql_text2;
      	    EXECUTE stmt2;
      	   
      	    PREPARE stmt3 FROM @sql_text3;
      	    EXECUTE stmt3;
      	   
      	   	PREPARE stmt4 FROM @sql_text4;
      	    EXECUTE stmt4;
      		
      	END LOOP;
      	
      	CLOSE PlotCursor;
      
      END;


## Exploratory SQL Used

      SELECT id, name, x_min, x_max, y_min, y_max, x_units, y_units, user_id, created_at, updated_at, plot_png, legend_png, plot_eps, legend_eps, no_id
      FROM RubyDB.plots
      where id = 109;
      
      ## Check if Limits are public, official and not personal
      SELECT distinct ld.*, l.official , l.public , l.result_type 
      FROM RubyDB.limit_displays ld, RubyDB.limits l
      where plot_id = 185 and ld.limit_id = l.id and (l.official = 1 or l.public = 1) and l.result_type != 'Personal'
      
      SELECT count(*)
      ##id, spin_dependency, result_type, measurement_type, x_units, y_units, x_rescale, y_rescale, data_label, file_name, data_comment, data_reference, experiment, rating, date_of_announcement, public, official, date_official, greatest_hit, date_of_run_start, date_of_run_end, `year`
      FROM RubyDB.limits
      where official = 1 and public = 1 and result_type != 'Personal'
      
      ##if result_type == 'Th' then fill else nofil
      ##if spin_dependency = 'SD' then dash
      ##if spin_dependency = 'SI' then line
      
      SELECT distinct ld.*, l.*
      FROM RubyDB.limit_displays ld, RubyDB.limits l
      where plot_id = 185 and ld.limit_id = l.id and (l.official = 1 or l.public = 1) and l.result_type != 'Personal' ##and ld.`style` = 'dash'
      
      select x.* FROM
      (
      SELECT ld.style, l.result_type , l.spin_dependency , ld.color, count(*) counter
      FROM RubyDB.limit_displays ld, RubyDB.limits l
      where ld.limit_id = l.id and (l.official = 1 or l.public = 1) and l.result_type != 'Personal' ##and ld.`style` = 'dash'
      group by ld.style, l.result_type , l.spin_dependency , ld.color
      ) x
      order by x.counter DESC 
