INSERT INTO `user_level_access` (`Title`, `Dashboard`, `Reception`, `Payment`, `Customer`, `Services`, `Sales`, `Inventory`, `Pet_Info`, `Report`, `User`, `Action`, `Gen_Settings`) VALUES
	('Owner', 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1),
	('Assistant', 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0),
	('Cashier', 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0),
	('Receptionist', 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0),
	('Service Provider', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

INSERT INTO `pet_breed` (`type`, `breed`) VALUES
	('Dog', 'Aspin'),
	('Cat', 'Puspin');

INSERT INTO `acc_cred` (`usn`, `pss`, `slt`, `entry_OTP`) VALUES
	('admin', '0c149295209d5f543cf1ba14956c5c135a78b9b311ad551715899e02c27dc99d', 'rCRF4amTSEOYQjqvWYuI7A==', NULL);

INSERT INTO `acc_info` (`usn`, `full_name`, `job_position`, `state`, `reason`) VALUES
	('admin', 'Administrator', 'Owner', 1, NULL);

INSERT INTO `categories` (`categ_name`, `does_expire`, `creator`, `state`, `Sellable`, `date_created`, `disabled_by`, `disabled_date`) VALUES
	('Accessories', 0, 'admin', 1, 1, CURRENT_DATE, NULL, NULL),
	('Medicine', 1, 'admin', 1, 1, CURRENT_DATE, NULL, NULL);

INSERT INTO `account_access_level` (`usn`, `Dashboard`, `Reception`, `Payment`, `Customer`, `Services`, `Sales`, `Inventory`, `Pet`, `Report`, `User`, `Settings`, `History`) VALUES
	('admin', 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0);