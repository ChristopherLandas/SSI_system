-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               11.1.2-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.3.0.6589
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping data for table ssi_test2.account_access_level: ~6 rows (approximately)
INSERT INTO `account_access_level` (`usn`, `Dashboard`, `Reception`, `Payment`, `Customer`, `Services`, `Sales`, `Inventory`, `Pet`, `Report`, `User`, `Settings`, `History`) VALUES
	('admin', 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0),
	('Cherie_Rejoy', 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0),
	('Christian', 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0),
	('Christian_Rubiales', 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0),
	('Clarence_Ugay', 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0),
	('James_Vinas', 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0),
	('Kajo_Baldisimo', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
	('Patrick_Feniza', 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0);

-- Dumping data for table ssi_test2.acc_cred: ~6 rows (approximately)
INSERT INTO `acc_cred` (`usn`, `pss`, `slt`, `entry_OTP`) VALUES
	('admin', '0c149295209d5f543cf1ba14956c5c135a78b9b311ad551715899e02c27dc99d', 'rCRF4amTSEOYQjqvWYuI7A==', NULL),
	('Cherie_Rejoy', '5eb3d84a14e6af8702ef7e1bf30975b483d2f1446415559a3b7c58df7fba1e86', 'rCk8PHXGTLSUDDL3Wr7lGQ==', NULL),
	('Christian', 'e37332cf7d736f380d73d3b9af4aec481dc88d4190d0e4080b30a12efc440e3c', '5iLVFj_qT--Pq_5YEXTtZQ==', NULL),
	('Christian_Rubiales', 'be9b9819707e880c88b663f27790b13b3ae5d5ba48122f02d0352da1ad2505e6', 'vCvLF9oKRtCXP5f2sD6TgQ==', NULL),
	('Clarence_Ugay', '507b9478277bbed2e689d741c856f6b87a01ed44be525b0ee7fd29b9a0261fd8', '7JnAPky_QfWdSHwJVpogog==', NULL),
	('James_Vinas', '99f30021a0ef61c233d57f674faf2f2acf76162179b2d358e48c81bf142dbbd0', 'ev4IQx6sTvW6X6dSwlvn1w==', NULL),
	('Kajo_Baldisimo', '78f7d7a56923f195db6d9ad702f2472b48724d6191343b6b99dcd0a1620d3081', '9YRNhbIBRxe8IBf3eV_pgA==', NULL),
	('Patrick_Feniza', '07321787528058748000c3b8258291c6d2eb6e6c18c8a770ca7c2570ae69ff2d', 'lph5QPCMQy2HCX8DY3GpVw==', NULL);

-- Dumping data for table ssi_test2.acc_info: ~7 rows (approximately)
INSERT INTO `acc_info` (`usn`, `full_name`, `job_position`, `state`, `reason`) VALUES
	('admin', 'Flex Flux', 'Owner', 1, NULL),
	('Cherie_Rejoy', 'Cherie Rejoy', 'Cashier', 1, NULL),
	('Christian', 'Christian', 'Assisstant', 0, 'Retired'),
	('Christian_Rubiales', 'Christian Rubiales', 'Reception', 1, NULL),
	('Clarence_Ugay', 'Clarence Ugay', 'Cashier', 0, 'Terminated'),
	('James_Vinas', 'James Vinas', 'Assisstant', 0, 'Terminated'),
	('Kajo_Baldisimo', 'Kajo Baldisimo', 'Service Provider', 0, 'Terminated'),
	('Patrick_Feniza', 'Patrick Feniza', 'Assisstant', 1, NULL);

-- Dumping data for table ssi_test2.action_history: ~5 rows (approximately)
INSERT INTO `action_history` (`Column 5`, `usn`, `Type`, `ACTION`, `action_date`) VALUES
	(309, 'admin', 'Item Encoding', 'ADD/admin/I6DC94', '2023-11-22 21:11:29'),
	(310, 'admin', 'Item Encoding', 'ADD/admin/I6DC94', '2023-11-22 21:12:33'),
	(311, 'admin', 'Item Encoding', 'ADD/admin/ID5590', '2023-11-22 21:27:21'),
	(312, 'admin', 'Service Encoding', 'ADDS/admin/S4293B', '2023-11-22 22:32:20'),
	(313, 'admin', 'Item Encoding', 'ADD/admin/ID5590', '2023-11-22 23:16:50'),
	(314, 'admin', 'Item Encoding', 'ADD/admin/I66D36', '2023-11-23 00:13:28');

-- Dumping data for table ssi_test2.categories: ~2 rows (approximately)
INSERT INTO `categories` (`categ_name`, `does_expire`, `creator`, `state`, `Sellable`, `date_created`, `disabled_by`, `disabled_date`) VALUES
	('Accessories', 0, 'admin', 1, 1, '2023-11-22 21:09:53', NULL, NULL),
	('Medicine', 1, 'admin', 1, 1, '2023-11-22 21:25:27', NULL, NULL);

-- Dumping data for table ssi_test2.disposal_history: ~0 rows (approximately)

-- Dumping data for table ssi_test2.invoice_item_content: ~0 rows (approximately)

-- Dumping data for table ssi_test2.invoice_record: ~0 rows (approximately)

-- Dumping data for table ssi_test2.invoice_service_content: ~0 rows (approximately)

-- Dumping data for table ssi_test2.item_general_info: ~2 rows (approximately)
INSERT INTO `item_general_info` (`UID`, `name`, `Category`, `brand`, `unit`, `added_by`, `added_date`, `updated_by`, `updated_date`) VALUES
	('I66D36', 'Cat Leash', 'Accessories', 'VetPlus', '3m', 'admin', '2023-11-23 00:12:19', NULL, NULL),
	('I6DC94', 'Flux Leash for Dogs', 'Accessories', 'VetPlus', '3m', 'admin', '2023-11-22 21:10:58', NULL, NULL),
	('ID5590', 'Flux Vitamins', 'Medicine', 'VetPlus', '10mg', 'admin', '2023-11-22 21:26:18', NULL, NULL);

-- Dumping data for table ssi_test2.item_inventory_info: ~8 rows (approximately)
INSERT INTO `item_inventory_info` (`id`, `UID`, `Stock`, `Expiry_Date`, `state`, `added_date`) VALUES
	(114, 'I6DC94', 10, NULL, 1, '2023-11-22'),
	(115, 'I6DC94', 5, NULL, 1, '2023-11-22'),
	(116, 'I6DC94', 8, NULL, 1, '2023-11-22'),
	(117, 'I6DC94', 2, NULL, 1, '2023-11-22'),
	(118, 'ID5590', 10, '2023-12-29', 1, '2023-11-22'),
	(119, 'ID5590', 5, '2023-12-29', 1, '2023-11-22'),
	(120, 'ID5590', 5, '2023-11-23', 1, '2023-11-22'),
	(121, 'I6DC94', 5, NULL, 1, '2023-11-22'),
	(122, 'I66D36', 10, NULL, 1, '2023-11-23');

-- Dumping data for table ssi_test2.item_settings: ~2 rows (approximately)
INSERT INTO `item_settings` (`UID`, `Cost_Price`, `Markup_Factor`, `Reorder_factor`, `Crit_factor`, `Safe_stock`, `rate_mode`) VALUES
	('I66D36', 100, 0.1, 0.85, 0.5, 10, 0),
	('I6DC94', 100, 0.1, 0.85, 0.5, 10, 0),
	('ID5590', 100, 0.2, 0.85, 0.5, 10, 0);

-- Dumping data for table ssi_test2.item_statistic_info: ~2 rows (approximately)
INSERT INTO `item_statistic_info` (`UID`, `month`, `monthly_average`, `rate_symbol`) VALUES
	('I6DC94', 11, 0, 'm'),
	('ID5590', 11, 0, 'm'),
	('I66D36', 11, 0, 'm');

-- Dumping data for table ssi_test2.item_supplier_info: ~0 rows (approximately)

-- Dumping data for table ssi_test2.item_transaction_content: ~0 rows (approximately)

-- Dumping data for table ssi_test2.login_report: ~0 rows (approximately)

-- Dumping data for table ssi_test2.log_history: ~2 rows (approximately)
INSERT INTO `log_history` (`usn`, `date_logged`, `time_in`, `time_out`) VALUES
	('admin', '2023-11-22', '22:31:31', '22:31:31'),
	('admin', '2023-11-22', '22:34:42', '22:34:42');

-- Dumping data for table ssi_test2.partially_recieving_item: ~3 rows (approximately)
INSERT INTO `partially_recieving_item` (`id`, `NAME`, `stock`, `supp_name`, `exp_date`, `reciever`, `date_recieved`) VALUES
	('RAB2F7', 'Flux Leash for Dogs (3m)', 5, 'MediCare Supplies', NULL, 'admin', '2023-11-22 00:00:00'),
	('R91686', 'Flux Leash for Dogs (3m)', 8, 'MediCare Supplies', NULL, 'admin', '2023-11-22 00:00:00'),
	('R3CD92', 'Flux Vitamins (10mg)', 5, 'MediCare Supplies', NULL, 'admin', '2023-11-22 00:00:00');

-- Dumping data for table ssi_test2.pet_breed: ~0 rows (approximately)

-- Dumping data for table ssi_test2.pet_info: ~0 rows (approximately)

-- Dumping data for table ssi_test2.pet_owner_info: ~1 rows (approximately)
INSERT INTO `pet_owner_info` (`owner_id`, `owner_name`, `address`, `contact_number`, `added_by`, `date_added`, `updated_by`, `updated_date`) VALUES
	('CU0F5386', 'Patrick Feniza', 'Fairveiw, Negros Occidental', '09785467891', 'admin', '2023-11-22 21:33:07', NULL, NULL);

-- Dumping data for table ssi_test2.receiving_history_info: ~6 rows (approximately)
INSERT INTO `receiving_history_info` (`receiving_id`, `order_quantity`, `receiver`, `expiry`, `date_received`) VALUES
	('RAB2F7', 5, 'admin', NULL, '2023-11-22 21:11:47'),
	('R91686', 8, 'admin', NULL, '2023-11-22 21:13:11'),
	('R91686', 2, 'admin', NULL, '2023-11-22 21:14:15'),
	('R3CD92', 5, 'admin', '2023-12-29', '2023-11-22 21:28:11'),
	('R3CD92', 5, 'admin', '2023-11-23', '2023-11-22 21:47:33'),
	('RAB2F7', 5, 'admin', NULL, '2023-11-22 23:09:03');

-- Dumping data for table ssi_test2.recieving_item: ~4 rows (approximately)
INSERT INTO `recieving_item` (`id`, `NAME`, `item_uid`, `ordered_by`, `initial_stock`, `current_stock`, `supp_id`, `exp_date`, `reciever`, `state`, `date_set`, `date_recieved`) VALUES
	('R3CD92', 'Flux Vitamins (10mg)', 'ID5590', 'admin', 10, 5, 'SUP00B9C', NULL, 'admin', 2, '2023-11-22 21:27:20', '2023-11-22 21:47:32'),
	('R3EEA7', 'Flux Vitamins (10mg)', 'ID5590', 'admin', 5, 5, 'SUP00B9C', NULL, NULL, 1, '2023-11-22 23:16:49', NULL),
	('R91686', 'Flux Leash for Dogs (3m)', 'I6DC94', 'admin', 10, 2, 'SUP00B9C', NULL, 'admin', 2, '2023-11-22 21:12:32', '2023-11-22 21:14:14'),
	('R95BDB', 'Cat Leash (3m)', 'I66D36', 'admin', 10, 10, 'SUP00B9C', NULL, NULL, 1, '2023-11-23 00:13:27', NULL),
	('RAB2F7', 'Flux Leash for Dogs (3m)', 'I6DC94', 'admin', 10, 5, 'SUP00B9C', NULL, 'admin', 2, '2023-11-22 21:11:27', '2023-11-22 23:09:02');

-- Dumping data for table ssi_test2.replacement_items: ~0 rows (approximately)

-- Dumping data for table ssi_test2.replacement_record: ~0 rows (approximately)

-- Dumping data for table ssi_test2.services_transaction_content: ~0 rows (approximately)

-- Dumping data for table ssi_test2.service_category_test: ~0 rows (approximately)

-- Dumping data for table ssi_test2.service_info: ~0 rows (approximately)

-- Dumping data for table ssi_test2.service_info_test: ~1 rows (approximately)
INSERT INTO `service_info_test` (`UID`, `service_name`, `price`, `category`, `duration_type`, `state`, `date_added`) VALUES
	('S4293B', 'Grooming', 500, NULL, 0, 1, '2023-11-22');

-- Dumping data for table ssi_test2.service_preceeding_schedule: ~0 rows (approximately)

-- Dumping data for table ssi_test2.supplier_info: ~1 rows (approximately)
INSERT INTO `supplier_info` (`supp_id`, `supp_name`, `telephone`, `contact_person`, `contact_number`, `contact_email`, `address`, `created_by`, `date_added`, `updated_by`, `date_modified`) VALUES
	('SUP00AB5', 'VetPlus Company', '7777-8888-9999', 'James Vinas', '09208902063', 'jamesvinas@vetplus.com', 'Tala, Caloocan City', 'admin', '2023-11-23 00:11:08', NULL, NULL),
	('SUP00B9C', 'MediCare Supplies', '8888-8888', 'Patrick Feniza', '09567894561', 'patrick_feniza@gmail.com', 'South Triangle,  Quezon City', 'admin', '2023-11-22 21:09:29', NULL, NULL);

-- Dumping data for table ssi_test2.supplier_item_info: ~2 rows (approximately)
INSERT INTO `supplier_item_info` (`supplier_id`, `item_id`, `active`) VALUES
	('SUP00B9C', 'I6DC94', 1),
	('SUP00B9C', 'ID5590', 1),
	('SUP00AB5', 'I66D36', 1),
	('SUP00B9C', 'I66D36', 1);

-- Dumping data for table ssi_test2.transaction_record: ~0 rows (approximately)

-- Dumping data for table ssi_test2.used_items_in_services: ~0 rows (approximately)

-- Dumping data for table ssi_test2.user_level_access: ~5 rows (approximately)
INSERT INTO `user_level_access` (`Title`, `Dashboard`, `Reception`, `Payment`, `Customer`, `Services`, `Sales`, `Inventory`, `Pet_Info`, `Report`, `User`, `Action`, `Gen_Settings`) VALUES
	('Assisstant', 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0),
	('Cashier', 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0),
	('Owner', 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1),
	('Reception', 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0),
	('Service Provider', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
