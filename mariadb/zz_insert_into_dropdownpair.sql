DELIMITER //

CREATE DEFINER='{$MARIADB_USERNAME}'@'%' PROCEDURE 'data'.'update_dropdownpair()
BEGIN

INSERT INTO data.dropdown_valuepair (variable,label,value,data_type) VALUES
	 ('official','All','0','boolean'),
	 ('official','Official','1','boolean'),
	 ('year','2000','2000','number'),
	 ('year','2001','2001','number'),
	 ('year','2002','2002','number'),
	 ('year','2003','2003','number'),
	 ('year','2004','2004','number'),
	 ('year','2005','2005','number'),
	 ('year','2006','2006','number'),
	 ('year','2007','2007','number');
INSERT INTO data.dropdown_valuepair (variable,label,value,data_type) VALUES
	 ('year','2008','2008','number'),
	 ('year','2009','2009','number'),
	 ('year','2010','2010','number'),
	 ('year','2011','2011','number'),
	 ('year','2012','2012','number'),
	 ('year','2013','2013','number'),
	 ('year','2014','2014','number'),
	 ('year','2015','2015','number'),
	 ('year','2016','2016','number'),
	 ('year','2017','2017','number');
INSERT INTO data.dropdown_valuepair (variable,label,value,data_type) VALUES
	 ('year','2018','2018','number'),
	 ('year','2019','2019','number'),
	 ('year','2020','2020','number'),
	 ('year','2021','2021','number'),
	 ('year','2022','2022','number'),
	 ('year','2023','2023','number'),
	 ('year','2024','2024','number'),
	 ('year','2025','2025','number'),
	 ('year','2026','2026','number'),
	 ('year','2027','2027','number');
INSERT INTO data.dropdown_valuepair (variable,label,value,data_type) VALUES
	 ('year','2028','2028','number'),
	 ('year','2029','2029','number'),
	 ('result_type','Theory','Th','text'),
	 ('result_type','Project','Proj','text'),
	 ('result_type','Experiment','Exp','text'),
	 ('spin_dependency','All','All','text'),
	 ('spin_dependency','spin-dependent','SD','text'),
	 ('spin_dependency','spin-independent','SI','text'),
	 ('greatest_hit','All','0','boolean'),
	 ('greatest_hit','Yes','1','boolean');
INSERT INTO data.dropdown_valuepair (variable,label,value,data_type) VALUES
	 ('experiment','CDMS I (SUF)','CDMS I (SUF)','text'),
	 ('experiment','CDMS II (Soudan)','CDMS II (Soudan)','text'),
	 ('experiment','SuperCDMS','SuperCDMS','text'),
	 ('experiment','LUX','LUX','text'),
	 ('experiment','XENON10','XENON10','text'),
	 ('experiment','XENON100','XENON100','text'),
	 ('experiment','XENON1T','XENON1T','text'),
	 ('experiment','ZEPLIN I','ZEPLIN I','text'),
	 ('experiment','ZEPLIN II','ZEPLIN II','text'),
	 ('experiment','ZEPLIN III','ZEPLIN III','text');
INSERT INTO data.dropdown_valuepair (variable,label,value,data_type) VALUES
	 ('experiment','ZEPLIN IV','ZEPLIN IV','text'),
	 ('experiment','COSME','COSME','text'),
	 ('experiment','CUORICINO','CUORICINO','text'),
	 ('experiment','DAMA','DAMA','text'),
	 ('experiment','KIMS DMRC','KIMS DMRC','text'),
	 ('experiment','ELEGANT V','ELEGANT V','text'),
	 ('experiment','Edelweiss','Edelweiss','text'),
	 ('experiment','GEDEON','GEDEON','text'),
	 ('experiment','Genius','Genius','text'),
	 ('experiment','Genino','Genino','text');
INSERT INTO data.dropdown_valuepair (variable,label,value,data_type) VALUES
	 ('experiment','Heidelberg','Heidelberg','text'),
	 ('experiment','IGEX','IGEX','text'),
	 ('experiment','KIMS','KIMS','text'),
	 ('experiment','MIBETA','MIBETA','text'),
	 ('experiment','Modane NaI','Modane NaI','text'),
	 ('experiment','NAIAD','NAIAD','text'),
	 ('experiment','PICASSO','PICASSO','text'),
	 ('experiment','ROSEBUD','ROSEBUD','text'),
	 ('experiment','SIMPLE','SIMPLE','text'),
	 ('experiment','Saclay','Saclay','text');
INSERT INTO data.dropdown_valuepair (variable,label,value,data_type) VALUES
	 ('experiment','SuperK','SuperK','text'),
	 ('experiment','TOKYO','TOKYO','text'),
	 ('experiment','UKDMC','UKDMC','text'),
	 ('experiment','WARP','WARP','text'),
	 ('experiment','Theory','Theory','text'),
	 ('experiment','Heidelberg-Moscow','Heidelberg-Moscow','text'),
	 ('experiment','Cuore','Cuore','text'),
	 ('experiment','DAMA Xe','DAMA Xe','text'),
	 ('experiment','TEXONO','TEXONO','text'),
	 ('experiment','XMASS','XMASS','text');
INSERT INTO data.dropdown_valuepair (variable,label,value,data_type) VALUES
	 ('experiment','IceCube','IceCube','text'),
	 ('experiment','DMTPC','DMTPC','text'),
	 ('experiment','DEAP CLEAN','DEAP CLEAN','text'),
	 ('experiment','DAMA/LIBRA','DAMA/LIBRA','text'),
	 ('experiment','CoGeNT','CoGeNT','text'),
	 ('experiment','COUPP','COUPP','text'),
	 ('experiment','LUX-ZEPLIN','LUX-ZEPLIN','text'),
	 ('experiment','Fermi','Fermi','text'),
	 ('experiment','DarkSide','DarkSide','text'),
	 ('experiment','DAMIC','DAMIC','text');
INSERT INTO data.dropdown_valuepair (variable,label,value,data_type) VALUES
	 ('experiment','EURECA','EURECA','text'),
	 ('experiment','DEAP-3600','DEAP-3600','text'),
	 ('experiment','PICO','PICO','text'),
	 ('experiment','PandaX','PandaX','text'),
	 ('experiment','LHC','LHC','text'),
	 ('experiment','DRIFT','DRIFT','text'),
	 ('experiment','GAMBIT','GAMBIT','text'),
	 ('experiment','CDEX-10','CDEX-10','text'),
	 ('experiment','NEWS-G','NEWS-G','text'),
	 ('experiment','XENONnT','XENONnT','text');
INSERT INTO data.dropdown_valuepair (variable,label,value,data_type) VALUES
	 ('experiment','CRESST','CRESST','text');


END;
//
DELIMITER ;
