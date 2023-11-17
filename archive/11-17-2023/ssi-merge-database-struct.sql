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


-- Dumping database structure for ssi_merged
CREATE DATABASE IF NOT EXISTS `ssi_merged` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `ssi_merged`; -- CHANGE THE NAME

-- Dumping structure for table ssi_merged.account_access_level
CREATE TABLE IF NOT EXISTS `account_access_level` (
  `usn` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
  `Dashboard` int(1) NOT NULL,
  `Reception` int(1) NOT NULL,
  `Payment` int(1) NOT NULL,
  `Customer` int(1) NOT NULL,
  `Services` int(1) NOT NULL,
  `Sales` int(1) NOT NULL,
  `Inventory` int(1) NOT NULL,
  `Pet` int(1) NOT NULL,
  `Report` int(1) NOT NULL,
  `User` int(1) NOT NULL,
  `Settings` int(1) NOT NULL,
  `History` int(1) NOT NULL,
  PRIMARY KEY (`usn`) USING BTREE,
  KEY `usn` (`usn`) USING BTREE,
  CONSTRAINT `account_access_level_ibfk_1` FOREIGN KEY (`usn`) REFERENCES `acc_cred` (`usn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.acc_cred
CREATE TABLE IF NOT EXISTS `acc_cred` (
  `usn` varchar(128) NOT NULL,
  `pss` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `slt` varchar(64) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `entry_OTP` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`usn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.acc_info
CREATE TABLE IF NOT EXISTS `acc_info` (
  `usn` varchar(128) NOT NULL,
  `full_name` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `job_position` varchar(32) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `state` int(1) NOT NULL,
  PRIMARY KEY (`usn`),
  KEY `job_position` (`job_position`),
  CONSTRAINT `acc_info_ibfk_1` FOREIGN KEY (`usn`) REFERENCES `acc_cred` (`usn`),
  CONSTRAINT `acc_info_ibfk_2` FOREIGN KEY (`job_position`) REFERENCES `user_level_access` (`Title`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.action_history
CREATE TABLE IF NOT EXISTS `action_history` (
  `Column 5` int(11) NOT NULL AUTO_INCREMENT,
  `usn` varchar(128) NOT NULL,
  `Type` varchar(25) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `ACTION` varchar(256) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `action_date` datetime NOT NULL,
  PRIMARY KEY (`Column 5`),
  KEY `usn` (`usn`),
  CONSTRAINT `action_history_ibfk_1` FOREIGN KEY (`usn`) REFERENCES `acc_cred` (`usn`)
) ENGINE=InnoDB AUTO_INCREMENT=286 DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.categories
CREATE TABLE IF NOT EXISTS `categories` (
  `categ_name` varchar(50) NOT NULL,
  `does_expire` int(1) NOT NULL,
  `creator` varchar(50) NOT NULL,
  `state` int(11) NOT NULL,
  `date_created` datetime DEFAULT NULL,
  `disabled_by` varchar(50) DEFAULT NULL,
  `disabled_date` datetime DEFAULT NULL,
  PRIMARY KEY (`categ_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.disposal_history
CREATE TABLE IF NOT EXISTS `disposal_history` (
  `id` varchar(8) NOT NULL DEFAULT '0',
  `receive_id` varchar(6) DEFAULT NULL,
  `item_uid` varchar(6) NOT NULL,
  `item_name` varchar(64) NOT NULL,
  `initial_quantity` int(11) DEFAULT NULL,
  `Current_quantity` int(11) DEFAULT NULL,
  `reason` varchar(50) NOT NULL,
  `date_of_disposal` datetime NOT NULL,
  `full_dispose_date` datetime DEFAULT NULL,
  `disposed_by` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `item_uid` (`item_uid`),
  CONSTRAINT `FK_disposal_history_item_general_info` FOREIGN KEY (`item_uid`) REFERENCES `item_general_info` (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.invoice_item_content
CREATE TABLE IF NOT EXISTS `invoice_item_content` (
  `invoice_uid` varchar(8) NOT NULL,
  `Item_uid` varchar(6) NOT NULL,
  `item_name` varchar(64) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` float NOT NULL,
  `deduction` float NOT NULL,
  KEY `invoice_uid` (`invoice_uid`),
  CONSTRAINT `invoice_item_content_ibfk_1` FOREIGN KEY (`invoice_uid`) REFERENCES `invoice_record` (`invoice_uid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.invoice_record
CREATE TABLE IF NOT EXISTS `invoice_record` (
  `invoice_uid` varchar(8) NOT NULL,
  `Attendant_usn` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
  `client_name` varchar(50) NOT NULL,
  `Total_amount` float NOT NULL,
  `payment_date` datetime DEFAULT NULL,
  `transaction_date` date NOT NULL,
  `State` int(1) NOT NULL DEFAULT 0,
  `Date_transacted` date DEFAULT NULL,
  `process_type` int(11) NOT NULL,
  PRIMARY KEY (`invoice_uid`),
  KEY `Attendant_usn` (`Attendant_usn`) USING BTREE,
  CONSTRAINT `invoice_record_ibfk_1` FOREIGN KEY (`Attendant_usn`) REFERENCES `acc_cred` (`usn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.invoice_service_content
CREATE TABLE IF NOT EXISTS `invoice_service_content` (
  `invoice_uid` varchar(8) NOT NULL,
  `service_uid` varchar(6) NOT NULL,
  `service_name` varchar(64) NOT NULL,
  `pet_uid` varchar(6) DEFAULT NULL,
  `patient_name` varchar(128) NOT NULL,
  `scheduled_date` date NOT NULL,
  `price` float NOT NULL,
  `deduction` float NOT NULL,
  `end_schedule` date DEFAULT NULL,
  `multiple_sched_quan` int(11) DEFAULT NULL,
  `instance_of_mul_sched` int(11) DEFAULT NULL,
  KEY `invoice_uid` (`invoice_uid`),
  KEY `FK_invoice_service_content_pet_info` (`pet_uid`),
  CONSTRAINT `FK_invoice_service_content_pet_info` FOREIGN KEY (`pet_uid`) REFERENCES `pet_info` (`id`) ON DELETE CASCADE,
  CONSTRAINT `invoice_service_content_ibfk_1` FOREIGN KEY (`invoice_uid`) REFERENCES `invoice_record` (`invoice_uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.item_general_info
CREATE TABLE IF NOT EXISTS `item_general_info` (
  `UID` varchar(6) NOT NULL,
  `name` varchar(64) NOT NULL,
  `Category` varchar(64) NOT NULL,
  `brand` varchar(50) NOT NULL,
  `unit` varchar(50) DEFAULT NULL,
  `added_by` varchar(50) NOT NULL,
  `added_date` datetime NOT NULL,
  `updated_by` varchar(50) DEFAULT NULL,
  `updated_date` datetime DEFAULT NULL,
  PRIMARY KEY (`UID`),
  KEY `Category` (`Category`),
  CONSTRAINT `item_general_info_ibfk_1` FOREIGN KEY (`Category`) REFERENCES `categories` (`categ_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.item_inventory_info
CREATE TABLE IF NOT EXISTS `item_inventory_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `UID` varchar(6) NOT NULL,
  `Stock` int(11) NOT NULL,
  `Expiry_Date` date DEFAULT NULL,
  `state` int(1) NOT NULL DEFAULT 1,
  `added_date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `UID` (`UID`),
  CONSTRAINT `item_inventory_info_ibfk_1` FOREIGN KEY (`UID`) REFERENCES `item_general_info` (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.item_settings
CREATE TABLE IF NOT EXISTS `item_settings` (
  `UID` varchar(6) NOT NULL,
  `Cost_Price` float NOT NULL,
  `Markup_Factor` float NOT NULL,
  `Reorder_factor` float NOT NULL,
  `Crit_factor` float NOT NULL,
  `Safe_stock` int(11) NOT NULL,
  `rate_mode` int(11) NOT NULL,
  PRIMARY KEY (`UID`),
  CONSTRAINT `item_settings_ibfk_1` FOREIGN KEY (`UID`) REFERENCES `item_general_info` (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.item_statistic_info
CREATE TABLE IF NOT EXISTS `item_statistic_info` (
  `UID` varchar(6) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `month` int(2) NOT NULL DEFAULT 0,
  `monthly_average` float NOT NULL DEFAULT 0,
  `rate_symbol` varchar(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT 'm',
  KEY `FK_item_statistic_info_item_general_info` (`UID`),
  CONSTRAINT `FK_item_statistic_info_item_general_info` FOREIGN KEY (`UID`) REFERENCES `item_general_info` (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.item_supplier_info
CREATE TABLE IF NOT EXISTS `item_supplier_info` (
  `UID` varchar(6) NOT NULL,
  `supp_id` varchar(8) NOT NULL,
  PRIMARY KEY (`UID`),
  KEY `supplier_info_fk` (`supp_id`) USING BTREE,
  CONSTRAINT `FK_item_supplier_info_supplier_info` FOREIGN KEY (`supp_id`) REFERENCES `supplier_info` (`supp_id`),
  CONSTRAINT `item_supplier_info_ibfk_1` FOREIGN KEY (`UID`) REFERENCES `item_general_info` (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.item_transaction_content
CREATE TABLE IF NOT EXISTS `item_transaction_content` (
  `transaction_uid` varchar(8) NOT NULL,
  `Item_uid` varchar(6) NOT NULL,
  `item_name` varchar(64) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` float NOT NULL,
  `deduction` float NOT NULL,
  `state` int(1) NOT NULL,
  KEY `FK_item_transaction_content_transaction_record` (`transaction_uid`),
  CONSTRAINT `FK_item_transaction_content_transaction_record` FOREIGN KEY (`transaction_uid`) REFERENCES `transaction_record` (`transaction_uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.login_report
CREATE TABLE IF NOT EXISTS `login_report` (
  `attempt_usn` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_cs DEFAULT NULL,
  `usn_used` varchar(128) NOT NULL,
  `date_created` datetime NOT NULL,
  KEY `attempt_usn` (`attempt_usn`),
  CONSTRAINT `login_report_ibfk_1` FOREIGN KEY (`attempt_usn`) REFERENCES `acc_cred` (`usn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.log_history
CREATE TABLE IF NOT EXISTS `log_history` (
  `usn` varchar(128) NOT NULL,
  `date_logged` date NOT NULL,
  `time_in` time NOT NULL,
  `time_out` time NOT NULL,
  KEY `usn` (`usn`),
  CONSTRAINT `log_history_ibfk_1` FOREIGN KEY (`usn`) REFERENCES `acc_cred` (`usn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;

-- Data exporting was unselected.

-- Dumping structure for procedure ssi_merged.newUser
DELIMITER //
CREATE PROCEDURE `newUser`()
BEGIN
    DECLARE newid INT;

    SET newid = 10;
    SELECT newid;
END//
DELIMITER ;

-- Dumping structure for table ssi_merged.partially_recieving_item
CREATE TABLE IF NOT EXISTS `partially_recieving_item` (
  `id` varchar(50) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
  `NAME` varchar(64) NOT NULL,
  `stock` int(11) NOT NULL,
  `supp_name` varchar(64) NOT NULL,
  `exp_date` date DEFAULT NULL,
  `reciever` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_cs DEFAULT NULL,
  `date_recieved` datetime DEFAULT NULL,
  KEY `FK_partially_recieving_item_recieving_item` (`id`),
  CONSTRAINT `FK_partially_recieving_item_recieving_item` FOREIGN KEY (`id`) REFERENCES `recieving_item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.pet_breed
CREATE TABLE IF NOT EXISTS `pet_breed` (
  `type` varchar(32) NOT NULL,
  `breed` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.pet_info
CREATE TABLE IF NOT EXISTS `pet_info` (
  `id` varchar(6) NOT NULL,
  `p_name` varchar(128) NOT NULL,
  `owner_id` varchar(8) NOT NULL,
  `breed` varchar(32) NOT NULL,
  `type` varchar(32) NOT NULL,
  `sex` varchar(12) NOT NULL,
  `weight` varchar(12) NOT NULL,
  `bday` date NOT NULL,
  `added_by` varchar(50) NOT NULL,
  `date_added` datetime NOT NULL,
  `updated_by` varchar(50) DEFAULT NULL,
  `updated_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `owner_id` (`owner_id`),
  CONSTRAINT `FK_pet_info_pet_owner_info` FOREIGN KEY (`owner_id`) REFERENCES `pet_owner_info` (`owner_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.pet_owner_info
CREATE TABLE IF NOT EXISTS `pet_owner_info` (
  `owner_id` varchar(8) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `owner_name` varchar(128) NOT NULL,
  `address` varchar(256) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `added_by` varchar(256) NOT NULL,
  `date_added` datetime NOT NULL,
  `updated_by` varchar(256) DEFAULT NULL,
  `updated_date` datetime DEFAULT NULL,
  PRIMARY KEY (`owner_id`),
  UNIQUE KEY `name` (`owner_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.receiving_history_info
CREATE TABLE IF NOT EXISTS `receiving_history_info` (
  `receiving_id` varchar(50) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
  `order_quantity` int(11) NOT NULL,
  `receiver` varchar(50) NOT NULL,
  `expiry` date DEFAULT NULL,
  `date_received` datetime NOT NULL,
  KEY `receiving_id` (`receiving_id`),
  CONSTRAINT `FK_receiving_history_info_recieving_item` FOREIGN KEY (`receiving_id`) REFERENCES `recieving_item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.recieving_item
CREATE TABLE IF NOT EXISTS `recieving_item` (
  `id` varchar(50) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
  `NAME` varchar(64) NOT NULL,
  `item_uid` varchar(6) NOT NULL,
  `ordered_by` varchar(128) NOT NULL,
  `initial_stock` int(11) NOT NULL,
  `current_stock` int(11) NOT NULL,
  `supp_id` varchar(8) NOT NULL,
  `exp_date` date DEFAULT NULL,
  `reciever` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_cs DEFAULT NULL,
  `state` int(1) NOT NULL,
  `date_set` datetime NOT NULL,
  `date_recieved` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_recieving_item_item_general_info` (`item_uid`),
  KEY `supp_id` (`supp_id`),
  CONSTRAINT `FK_recieving_item_item_general_info` FOREIGN KEY (`item_uid`) REFERENCES `item_general_info` (`UID`),
  CONSTRAINT `FK_recieving_item_supplier_info` FOREIGN KEY (`supp_id`) REFERENCES `supplier_info` (`supp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.replacement_items
CREATE TABLE IF NOT EXISTS `replacement_items` (
  `rep_id` varchar(12) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `item_id` varchar(6) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `item_desc` varchar(256) NOT NULL,
  `price` float NOT NULL,
  `quantity` int(11) NOT NULL,
  `reason` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.replacement_record
CREATE TABLE IF NOT EXISTS `replacement_record` (
  `rep_id` varchar(12) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `transction_id` varchar(8) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `new_total` float NOT NULL,
  `replace_by` varchar(12) NOT NULL,
  `replacement_date` datetime NOT NULL,
  PRIMARY KEY (`rep_id`),
  KEY `transction_id` (`transction_id`),
  CONSTRAINT `FK_replacement_record_transaction_record` FOREIGN KEY (`transction_id`) REFERENCES `transaction_record` (`transaction_uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.services_transaction_content
CREATE TABLE IF NOT EXISTS `services_transaction_content` (
  `transaction_uid` varchar(8) NOT NULL,
  `service_uid` varchar(6) NOT NULL,
  `service_name` varchar(64) NOT NULL,
  `pet_uid` varchar(6) NOT NULL,
  `patient_name` varchar(128) NOT NULL,
  `scheduled_date` date NOT NULL,
  `price` float NOT NULL,
  `deduction` float NOT NULL,
  `status` int(11) NOT NULL,
  `end_schedule` date DEFAULT NULL,
  `multiple_sched_quan` int(11) DEFAULT NULL,
  `instance_of_mul_sched` int(11) DEFAULT NULL,
  `service_provider` varchar(265) DEFAULT NULL,
  KEY `transaction_uid` (`transaction_uid`),
  KEY `FK_services_transaction_content_pet_info` (`pet_uid`),
  CONSTRAINT `FK_services_transaction_content_pet_info` FOREIGN KEY (`pet_uid`) REFERENCES `pet_info` (`id`),
  CONSTRAINT `FK_services_transaction_content_transaction_record` FOREIGN KEY (`transaction_uid`) REFERENCES `transaction_record` (`transaction_uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.service_category_test
CREATE TABLE IF NOT EXISTS `service_category_test` (
  `category` varchar(64) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `state` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.service_info
CREATE TABLE IF NOT EXISTS `service_info` (
  `UID` varchar(6) NOT NULL,
  `service_name` varchar(256) NOT NULL,
  `Item_needed` varchar(512) NOT NULL,
  `price` float NOT NULL,
  `state` int(1) NOT NULL,
  `date_added` date NOT NULL,
  PRIMARY KEY (`UID`),
  UNIQUE KEY `service_name` (`service_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.service_info_test
CREATE TABLE IF NOT EXISTS `service_info_test` (
  `UID` varchar(6) NOT NULL,
  `service_name` varchar(256) NOT NULL,
  `price` float NOT NULL,
  `category` varchar(64) DEFAULT '',
  `duration_type` int(1) NOT NULL,
  `state` int(1) NOT NULL,
  `date_added` date NOT NULL,
  PRIMARY KEY (`UID`) USING BTREE,
  UNIQUE KEY `service_name` (`service_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci ROW_FORMAT=DYNAMIC;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.service_preceeding_schedule
CREATE TABLE IF NOT EXISTS `service_preceeding_schedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `transaction_uid` varchar(8) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL DEFAULT '0',
  `service_uid` varchar(6) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `service_name` varchar(256) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `prefix` varchar(50) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `scheduled_date` date NOT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `FK__services_transaction_content` (`transaction_uid`) USING BTREE,
  KEY `FK__service_info_test` (`service_uid`) USING BTREE,
  CONSTRAINT `FK__service_info_test` FOREIGN KEY (`service_uid`) REFERENCES `service_info_test` (`UID`),
  CONSTRAINT `FK__services_transaction_content` FOREIGN KEY (`transaction_uid`) REFERENCES `services_transaction_content` (`transaction_uid`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.supplier_info
CREATE TABLE IF NOT EXISTS `supplier_info` (
  `supp_id` varchar(8) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `supp_name` varchar(128) NOT NULL,
  `telephone` varchar(50) NOT NULL,
  `contact_person` varchar(128) NOT NULL,
  `contact_number` varchar(32) NOT NULL,
  `contact_email` varchar(128) DEFAULT NULL,
  `address` varchar(256) NOT NULL,
  `created_by` varchar(128) NOT NULL,
  `date_added` datetime NOT NULL,
  `updated_by` varchar(128) DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  PRIMARY KEY (`supp_id`),
  UNIQUE KEY `supp_name` (`supp_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.supplier_item_info
CREATE TABLE IF NOT EXISTS `supplier_item_info` (
  `supplier_id` varchar(8) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `item_id` varchar(6) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `active` int(1) NOT NULL DEFAULT 1,
  KEY `supplier_id` (`supplier_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `FK_supplier_item_info_item_general_info` FOREIGN KEY (`item_id`) REFERENCES `item_general_info` (`UID`),
  CONSTRAINT `FK_supplier_item_info_supplier_info` FOREIGN KEY (`supplier_id`) REFERENCES `supplier_info` (`supp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.transaction_record
CREATE TABLE IF NOT EXISTS `transaction_record` (
  `transaction_uid` varchar(8) NOT NULL,
  `Attendant_usn` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
  `Client_id` varchar(50) DEFAULT NULL,
  `client_name` varchar(50) DEFAULT NULL,
  `Total_amount` float NOT NULL,
  `transaction_date` date NOT NULL,
  `state` int(1) NOT NULL,
  `deduction` float DEFAULT NULL,
  PRIMARY KEY (`transaction_uid`),
  KEY `Attendant_usn` (`Attendant_usn`),
  CONSTRAINT `transaction_record_ibfk_1` FOREIGN KEY (`Attendant_usn`) REFERENCES `acc_cred` (`usn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table ssi_merged.user_level_access
CREATE TABLE IF NOT EXISTS `user_level_access` (
  `Title` varchar(32) NOT NULL,
  `add_item` int(1) NOT NULL,
  `Dashboard` int(1) NOT NULL,
  `Reception` int(1) NOT NULL,
  `Payment` int(1) NOT NULL,
  `Services` int(1) NOT NULL,
  `Sales` int(1) NOT NULL,
  `Inventory` int(1) NOT NULL,
  `Pet_Info` int(1) NOT NULL,
  `Report` int(1) NOT NULL,
  `User` int(1) NOT NULL,
  `Action` int(1) NOT NULL,
  `Gen_Settings` int(11) NOT NULL,
  PRIMARY KEY (`Title`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Data exporting was unselected.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
