-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.6.11-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for ssi
CREATE DATABASE IF NOT EXISTS `ssi` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `ssi`;

-- Dumping structure for table ssi.acc_cred
CREATE TABLE IF NOT EXISTS `acc_cred` (
  `usn` varchar(128) NOT NULL,
  `pss` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `slt` varchar(64) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `entry_OTP` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`usn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;

-- Dumping data for table ssi.acc_cred: ~3 rows (approximately)
/*!40000 ALTER TABLE `acc_cred` DISABLE KEYS */;
INSERT INTO `acc_cred` (`usn`, `pss`, `slt`, `entry_OTP`) VALUES
	('admin', '0c149295209d5f543cf1ba14956c5c135a78b9b311ad551715899e02c27dc99d', 'rCRF4amTSEOYQjqvWYuI7A==', NULL),
	('assisstant', '5362ca593f063f2581f756e9827bdd02da670bad2b176108380d7bc971ee5148', 'ljEGlbKwSZe3ECK-0b2K8g==', NULL);
/*!40000 ALTER TABLE `acc_cred` ENABLE KEYS */;

-- Dumping structure for table ssi.acc_info
CREATE TABLE IF NOT EXISTS `acc_info` (
  `usn` varchar(128) NOT NULL,
  `full_name` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `job_position` varchar(32) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  PRIMARY KEY (`usn`),
  KEY `job_position` (`job_position`),
  CONSTRAINT `acc_info_ibfk_1` FOREIGN KEY (`usn`) REFERENCES `acc_cred` (`usn`),
  CONSTRAINT `acc_info_ibfk_2` FOREIGN KEY (`job_position`) REFERENCES `user_level_access` (`Title`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;

-- Dumping data for table ssi.acc_info: ~2 rows (approximately)
/*!40000 ALTER TABLE `acc_info` DISABLE KEYS */;
INSERT INTO `acc_info` (`usn`, `full_name`, `job_position`) VALUES
	('admin', 'Owner', 'Owner'),
	('assisstant', 'Assisstant', 'Assisstant');
/*!40000 ALTER TABLE `acc_info` ENABLE KEYS */;

-- Dumping structure for table ssi.action_history
CREATE TABLE IF NOT EXISTS `action_history` (
  `usn` varchar(128) NOT NULL,
  `ACTION` varchar(256) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `action_date` date NOT NULL,
  PRIMARY KEY (`usn`),
  CONSTRAINT `action_history_ibfk_1` FOREIGN KEY (`usn`) REFERENCES `acc_cred` (`usn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;

-- Dumping data for table ssi.action_history: ~0 rows (approximately)
/*!40000 ALTER TABLE `action_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `action_history` ENABLE KEYS */;

-- Dumping structure for table ssi.categories
CREATE TABLE IF NOT EXISTS `categories` (
  `categ_name` varchar(50) NOT NULL,
  `does_expire` int(1) DEFAULT NULL,
  PRIMARY KEY (`categ_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi.categories: ~4 rows (approximately)
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` (`categ_name`, `does_expire`) VALUES
	('Accessories', 0),
	('Food', 1),
	('Medicine', 1),
	('test', 0);
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;

-- Dumping structure for table ssi.disposal_history
CREATE TABLE IF NOT EXISTS `disposal_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_name` varchar(64) NOT NULL,
  `quan` int(11) NOT NULL,
  `date_of_disposal` datetime NOT NULL,
  `disposed_by` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi.disposal_history: ~1 rows (approximately)
/*!40000 ALTER TABLE `disposal_history` DISABLE KEYS */;
INSERT INTO `disposal_history` (`id`, `item_name`, `quan`, `date_of_disposal`, `disposed_by`) VALUES
	(1, 'MayPaw Heavy Duty Rope Dog Leash', 12, '2023-06-11 03:22:39', 'klyde');
/*!40000 ALTER TABLE `disposal_history` ENABLE KEYS */;

-- Dumping structure for table ssi.item_general_info
CREATE TABLE IF NOT EXISTS `item_general_info` (
  `UID` varchar(6) NOT NULL,
  `name` varchar(64) NOT NULL,
  `Category` varchar(64) NOT NULL,
  PRIMARY KEY (`UID`),
  KEY `Category` (`Category`),
  CONSTRAINT `item_general_info_ibfk_1` FOREIGN KEY (`Category`) REFERENCES `categories` (`categ_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi.item_general_info: ~5 rows (approximately)
/*!40000 ALTER TABLE `item_general_info` DISABLE KEYS */;
INSERT INTO `item_general_info` (`UID`, `name`, `Category`) VALUES
	('I00001', 'MayPaw Heavy Duty Rope Dog Leash', 'Accessories'),
	('I00002', 'Taglory Rope Dog Leash', 'Accessories'),
	('I00003', 'Fresh Step Clumping Cat Litter', 'Accessories'),
	('I00004', 'Fresh Step LeightWeight Clumping Cat Litter', 'Accessories'),
	('I00005', 'Nutri-Vet Bladder Control Supplement for Dogs', 'Medicine');
/*!40000 ALTER TABLE `item_general_info` ENABLE KEYS */;

-- Dumping structure for table ssi.item_inventory_info
CREATE TABLE IF NOT EXISTS `item_inventory_info` (
  `UID` varchar(6) NOT NULL,
  `Stock` int(11) NOT NULL,
  `Expiry_Date` date DEFAULT NULL,
  KEY `UID` (`UID`),
  CONSTRAINT `item_inventory_info_ibfk_1` FOREIGN KEY (`UID`) REFERENCES `item_general_info` (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi.item_inventory_info: ~7 rows (approximately)
/*!40000 ALTER TABLE `item_inventory_info` DISABLE KEYS */;
INSERT INTO `item_inventory_info` (`UID`, `Stock`, `Expiry_Date`) VALUES
	('I00001', 791, NULL),
	('I00002', 50, NULL),
	('I00003', 66, NULL),
	('I00004', 60, NULL),
	('I00005', 24, '2023-10-26'),
	('I00005', 48, '2023-06-13'),
	('I00005', 1, '2023-06-17');
/*!40000 ALTER TABLE `item_inventory_info` ENABLE KEYS */;

-- Dumping structure for table ssi.item_settings
CREATE TABLE IF NOT EXISTS `item_settings` (
  `UID` varchar(6) NOT NULL,
  `Cost_Price` float NOT NULL,
  `Markup_Factor` float NOT NULL,
  `Reorder_factor` float NOT NULL,
  `Crit_factor` float NOT NULL,
  `Safe_stock` int(11) NOT NULL,
  PRIMARY KEY (`UID`),
  CONSTRAINT `item_settings_ibfk_1` FOREIGN KEY (`UID`) REFERENCES `item_general_info` (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi.item_settings: ~5 rows (approximately)
/*!40000 ALTER TABLE `item_settings` DISABLE KEYS */;
INSERT INTO `item_settings` (`UID`, `Cost_Price`, `Markup_Factor`, `Reorder_factor`, `Crit_factor`, `Safe_stock`) VALUES
	('I00001', 475, 0.1, 0.85, 0.5, 50),
	('I00002', 400, 0.1, 0.85, 0.5, 50),
	('I00003', 525, 0.1, 0.85, 0.5, 25),
	('I00004', 724.5, 0.1, 0.85, 0.5, 25),
	('I00005', 1036.5, 0.1, 0.85, 0.5, 85);
/*!40000 ALTER TABLE `item_settings` ENABLE KEYS */;

-- Dumping structure for table ssi.item_supplier_info
CREATE TABLE IF NOT EXISTS `item_supplier_info` (
  `UID` varchar(6) NOT NULL,
  `Supplier` varchar(64) NOT NULL,
  `Contacts` varchar(64) NOT NULL,
  PRIMARY KEY (`UID`),
  CONSTRAINT `item_supplier_info_ibfk_1` FOREIGN KEY (`UID`) REFERENCES `item_general_info` (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi.item_supplier_info: ~5 rows (approximately)
/*!40000 ALTER TABLE `item_supplier_info` DISABLE KEYS */;
INSERT INTO `item_supplier_info` (`UID`, `Supplier`, `Contacts`) VALUES
	('I00001', 'ABC corp.', 'ABCcorp@gmail.com'),
	('I00002', 'ABC corp.', 'ABCcorp@gmail.com'),
	('I00003', 'medVet assc.', '+639042648221'),
	('I00004', 'medVet assc..', '+639042648221'),
	('I00005', 'Pfizer corp..', 'OrtSupp@Pfizer.com.ph');
/*!40000 ALTER TABLE `item_supplier_info` ENABLE KEYS */;

-- Dumping structure for table ssi.item_transaction_content
CREATE TABLE IF NOT EXISTS `item_transaction_content` (
  `transaction_uid` varchar(8) NOT NULL,
  `Item_uid` varchar(6) NOT NULL,
  `item_name` varchar(64) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` float NOT NULL,
  `deduction` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi.item_transaction_content: ~18 rows (approximately)
/*!40000 ALTER TABLE `item_transaction_content` DISABLE KEYS */;
INSERT INTO `item_transaction_content` (`transaction_uid`, `Item_uid`, `item_name`, `quantity`, `price`, `deduction`) VALUES
	('0', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('0', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('2', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('4', 'I00002', 'Taglory Rope Dog Leash', 5, 440, 0),
	('8', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 2, 522.5, 0),
	('9', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('13', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('16', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('18', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('19', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('20', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('21', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('23', 'I00008', 'TestItem', 50, 600, 0),
	('29', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('30', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('32', 'I00004', 'Fresh Step LeightWeight Clumping Cat Litter', 17, 796.95, 0),
	('33', 'I00005', 'Nutri-Vet Bladder Control Supplement for Dogs', 1, 1140.15, 0),
	('34', 'I00005', 'Nutri-Vet Bladder Control Supplement for Dogs', 1, 1140.15, 0),
	('35', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('37', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0);
/*!40000 ALTER TABLE `item_transaction_content` ENABLE KEYS */;

-- Dumping structure for table ssi.login_report
CREATE TABLE IF NOT EXISTS `login_report` (
  `attempt_usn` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_cs DEFAULT NULL,
  `usn_used` varchar(128) NOT NULL,
  `date_created` datetime NOT NULL,
  KEY `attempt_usn` (`attempt_usn`),
  CONSTRAINT `login_report_ibfk_1` FOREIGN KEY (`attempt_usn`) REFERENCES `acc_cred` (`usn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi.login_report: ~2 rows (approximately)
/*!40000 ALTER TABLE `login_report` DISABLE KEYS */;
INSERT INTO `login_report` (`attempt_usn`, `usn_used`, `date_created`) VALUES
	(NULL, 'admin', '2023-06-07 23:50:59'),
	('admin', 'admin', '2023-06-07 23:54:09'),
	('admin', 'admin', '2023-06-07 23:55:45');
/*!40000 ALTER TABLE `login_report` ENABLE KEYS */;

-- Dumping structure for table ssi.log_history
CREATE TABLE IF NOT EXISTS `log_history` (
  `usn` varchar(128) NOT NULL,
  `date_logged` date NOT NULL,
  `time_in` time NOT NULL,
  `time_out` time NOT NULL,
  KEY `usn` (`usn`),
  CONSTRAINT `log_history_ibfk_1` FOREIGN KEY (`usn`) REFERENCES `acc_cred` (`usn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;

-- Dumping data for table ssi.log_history: ~64 rows (approximately)
/*!40000 ALTER TABLE `log_history` DISABLE KEYS */;
INSERT INTO `log_history` (`usn`, `date_logged`, `time_in`, `time_out`) VALUES
	('admin', '2023-05-29', '22:34:57', '22:34:57'),
	('admin', '2023-05-29', '22:37:24', '22:37:24'),
	('admin', '2023-05-29', '22:38:22', '22:38:22'),
	('admin', '2023-05-29', '22:39:13', '22:39:13'),
	('admin', '2023-05-29', '22:39:36', '22:39:36'),
	('admin', '2023-05-29', '22:40:29', '22:40:29'),
	('admin', '2023-06-02', '14:19:46', '14:19:46'),
	('admin', '2023-06-02', '14:21:26', '14:21:26'),
	('admin', '2023-06-02', '14:22:06', '14:22:06'),
	('admin', '2023-06-02', '14:26:13', '14:26:13'),
	('admin', '2023-06-02', '14:28:48', '14:28:48'),
	('admin', '2023-06-02', '14:29:47', '14:29:47'),
	('admin', '2023-06-02', '14:33:59', '14:33:59'),
	('admin', '2023-06-02', '14:39:50', '14:39:50'),
	('admin', '2023-06-02', '14:40:42', '14:40:42'),
	('admin', '2023-06-02', '14:42:38', '14:42:38'),
	('admin', '2023-06-02', '14:46:21', '14:46:21'),
	('admin', '2023-06-02', '14:47:25', '14:47:25'),
	('admin', '2023-06-02', '14:48:11', '14:48:11'),
	('admin', '2023-06-02', '14:48:59', '14:48:59'),
	('admin', '2023-06-02', '14:50:23', '14:50:23'),
	('admin', '2023-06-02', '14:51:33', '14:51:33'),
	('admin', '2023-06-02', '15:02:27', '15:02:27'),
	('admin', '2023-06-02', '15:03:45', '15:03:45'),
	('admin', '2023-06-02', '15:04:37', '15:04:37'),
	('admin', '2023-06-02', '15:07:48', '15:07:48'),
	('admin', '2023-06-02', '15:09:33', '15:09:33'),
	('admin', '2023-06-02', '15:14:38', '15:14:38'),
	('admin', '2023-06-02', '15:16:19', '15:16:19'),
	('admin', '2023-06-02', '15:18:39', '15:18:39'),
	('admin', '2023-06-02', '15:20:53', '15:25:45'),
	('admin', '2023-06-02', '15:30:11', '15:30:11'),
	('admin', '2023-06-02', '15:47:50', '15:47:50'),
	('admin', '2023-06-02', '15:48:36', '15:48:36'),
	('admin', '2023-06-02', '15:49:11', '16:14:40'),
	('admin', '2023-06-04', '02:13:44', '02:13:44'),
	('admin', '2023-06-04', '02:14:56', '02:14:56'),
	('admin', '2023-06-04', '02:15:42', '02:15:42'),
	('admin', '2023-06-04', '02:16:38', '02:16:38'),
	('admin', '2023-06-04', '02:18:20', '02:18:20'),
	('admin', '2023-06-04', '02:21:02', '02:21:02'),
	('admin', '2023-06-04', '02:23:31', '02:23:31'),
	('admin', '2023-06-04', '02:24:46', '02:24:46'),
	('admin', '2023-06-04', '02:25:58', '02:27:23'),
	('admin', '2023-06-04', '02:28:13', '02:28:31'),
	('admin', '2023-06-04', '02:28:35', '02:28:35'),
	('admin', '2023-06-06', '15:13:12', '15:13:12'),
	('admin', '2023-06-06', '15:41:05', '15:41:05'),
	('admin', '2023-06-06', '15:41:53', '15:41:53'),
	('admin', '2023-06-07', '03:25:37', '03:25:37'),
	('admin', '2023-06-07', '03:47:32', '04:25:44'),
	('admin', '2023-06-07', '07:33:51', '07:34:31'),
	('admin', '2023-06-07', '09:46:08', '09:46:08'),
	('admin', '2023-06-07', '09:48:57', '09:48:57'),
	('admin', '2023-06-07', '09:51:04', '09:51:04'),
	('admin', '2023-06-07', '09:52:27', '09:52:27'),
	('admin', '2023-06-07', '10:00:43', '10:00:43'),
	('admin', '2023-06-07', '10:01:37', '10:01:37'),
	('admin', '2023-06-07', '10:03:46', '10:03:46'),
	('admin', '2023-06-07', '10:07:02', '10:07:02'),
	('admin', '2023-06-07', '10:08:37', '10:08:37'),
	('admin', '2023-06-07', '10:13:34', '10:17:21'),
	('admin', '2023-06-07', '10:34:57', '10:36:22'),
	('admin', '2023-06-07', '10:36:26', '18:56:06'),
	('admin', '2023-06-07', '10:36:49', '18:55:17');
/*!40000 ALTER TABLE `log_history` ENABLE KEYS */;

-- Dumping structure for table ssi.recieving_item
CREATE TABLE IF NOT EXISTS `recieving_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(64) NOT NULL,
  `stock` int(11) NOT NULL,
  `supp_name` varchar(64) NOT NULL,
  `exp_date` date DEFAULT NULL,
  `reciever` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_cs DEFAULT NULL,
  `state` int(1) NOT NULL,
  `date_recieved` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi.recieving_item: ~2 rows (approximately)
/*!40000 ALTER TABLE `recieving_item` DISABLE KEYS */;
INSERT INTO `recieving_item` (`id`, `NAME`, `stock`, `supp_name`, `exp_date`, `reciever`, `state`, `date_recieved`) VALUES
	(1, 'Nutri-Vet Bladder Control Supplement for Dogs', 15, 'Pfizer corp..', '2023-08-24', NULL, 1, NULL),
	(2, 'Nutri-Vet Bladder Control Supplement for Dogs', 25, 'Pfizer corp..', '2023-08-03', NULL, 1, NULL);
/*!40000 ALTER TABLE `recieving_item` ENABLE KEYS */;

-- Dumping structure for table ssi.services_transaction_content
CREATE TABLE IF NOT EXISTS `services_transaction_content` (
  `transaction_uid` varchar(8) NOT NULL,
  `service_uid` varchar(6) NOT NULL,
  `service_name` varchar(64) NOT NULL,
  `patient_name` varchar(128) NOT NULL,
  `scheduled_date` date NOT NULL,
  `price` float NOT NULL,
  `deduction` float NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi.services_transaction_content: ~17 rows (approximately)
/*!40000 ALTER TABLE `services_transaction_content` DISABLE KEYS */;
INSERT INTO `services_transaction_content` (`transaction_uid`, `service_uid`, `service_name`, `patient_name`, `scheduled_date`, `price`, `deduction`, `status`) VALUES
	('1', 'S00001', 'Grooming', 'test', '2023-06-06', 500, 0, 0),
	('3', 'S00001', 'Grooming', 'Rexie C.', '2023-06-06', 500, 0, 0),
	('4', 'S00003', 'Papiloma Vaccine', 'TJOEL10', '2023-06-06', 2500, 0, 0),
	('4', 'S00002', '5-in-1 Vaccine', 'TJOEL10', '2023-06-06', 1500, 0, 0),
	('5', 'S00001', 'Grooming', 'rex', '2023-06-07', 500, 0, 0),
	('9', 'S00001', 'Grooming', 'rex', '2023-07-26', 500, 0, 0),
	('10', 'S00001', 'Grooming', 'rex', '2023-07-26', 500, 0, 0),
	('11', 'S00006', 'Confinement', 'rex', '2023-07-26', 200, 0, 0),
	('12', 'S00001', 'Grooming', 'rex', '2023-07-26', 500, 0, 0),
	('13', 'S00001', 'Grooming', 'rex1', '2023-09-28', 500, 0, 0),
	('16', 'S00001', 'Grooming', 'rex', '2023-08-31', 500, 0, 0),
	('17', 'S00006', 'Confinement', 'rex', '2023-08-24', 200, 0, 0),
	('22', 'S00005', 'Canine Castration Surgery', 'rex', '2023-09-28', 1700, 0, 0),
	('24', 'S00001', 'Grooming', 'rex', '2023-08-31', 500, 0, 0),
	('25', 'S00001', 'Grooming', 'rex', '2023-06-29', 500, 0, 0),
	('26', 'S00002', '5-in-1 Vaccine', 'rex', '2023-09-28', 1500, 0, 0),
	('27', 'S00001', 'Grooming', 'rex', '2023-07-27', 500, 0, 0),
	('28', 'S00001', 'Grooming', 'rex', '2023-08-31', 500, 0, 0),
	('31', 'S00001', 'Grooming', 'rex', '2023-09-21', 500, 0, 0),
	('36', 'S00002', '5-in-1 Vaccine', 'rex', '2023-06-29', 1500, 0, 0);
/*!40000 ALTER TABLE `services_transaction_content` ENABLE KEYS */;

-- Dumping structure for table ssi.service_info
CREATE TABLE IF NOT EXISTS `service_info` (
  `UID` varchar(6) NOT NULL,
  `service_name` varchar(256) NOT NULL,
  `Item_needed` varchar(512) NOT NULL,
  `price` float NOT NULL,
  `state` int(1) NOT NULL,
  `date_added` date NOT NULL,
  PRIMARY KEY (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi.service_info: ~8 rows (approximately)
/*!40000 ALTER TABLE `service_info` DISABLE KEYS */;
INSERT INTO `service_info` (`UID`, `service_name`, `Item_needed`, `price`, `state`, `date_added`) VALUES
	('S00001', 'Grooming', 'test', 500, 1, '2023-05-29'),
	('S00002', '5-in-1 Vaccine', 'test', 1500, 1, '2023-05-29'),
	('S00003', 'Papiloma Vaccine', 'test', 2500, 1, '2023-05-29'),
	('S00004', 'Yeast Infection Treatment', 'test', 2100, 1, '2023-05-29'),
	('S00005', 'Canine Castration Surgery', 'test', 1700, 1, '2023-05-29'),
	('S00006', 'Confinement', 'test', 200, 1, '2023-05-29'),
	('S00007', 'Euthanasion', 'test', 900, 1, '2023-05-29'),
	('S00008', 'Feline Castration Srugery', 'test', 500, 1, '2023-05-29');
/*!40000 ALTER TABLE `service_info` ENABLE KEYS */;

-- Dumping structure for table ssi.transaction_record
CREATE TABLE IF NOT EXISTS `transaction_record` (
  `transaction_uid` varchar(8) NOT NULL,
  `Attendant_usn` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
  `client_name` varchar(50) NOT NULL,
  `Total_amount` float NOT NULL,
  `transaction_date` date NOT NULL,
  KEY `Attendant_usn` (`Attendant_usn`),
  CONSTRAINT `transaction_record_ibfk_1` FOREIGN KEY (`Attendant_usn`) REFERENCES `acc_cred` (`usn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi.transaction_record: ~35 rows (approximately)
/*!40000 ALTER TABLE `transaction_record` DISABLE KEYS */;
INSERT INTO `transaction_record` (`transaction_uid`, `Attendant_usn`, `client_name`, `Total_amount`, `transaction_date`) VALUES
	('0', 'admin', 'gege', 522.5, '2023-06-06'),
	('1', 'admin', 'test', 500, '2023-06-06'),
	('2', 'admin', 'rgtn', 522.5, '2023-06-06'),
	('3', 'admin', 'Rexie C.', 500, '2023-06-06'),
	('4', 'admin', 'TJOEL10', 6200, '2023-06-06'),
	('5', 'admin', 'rex', 500, '2023-06-07'),
	('6', 'admin', 'rex', 1500, '2023-06-07'),
	('7', 'admin', 'rex', 500, '2023-06-07'),
	('8', 'admin', 'rex', 1545, '2023-06-07'),
	('9', 'admin', 'rex', 1022.5, '2023-06-07'),
	('10', 'admin', 'rex', 500, '2023-06-07'),
	('11', 'admin', 'rex', 200, '2023-06-07'),
	('12', 'admin', 'rex', 500, '2023-06-07'),
	('13', 'admin', 'rex1', 1022.5, '2023-06-07'),
	('14', 'admin', 'rex1', 1700, '2023-06-07'),
	('15', 'admin', 'rex1', 1700, '2023-06-07'),
	('16', 'admin', 'rex', 1022.5, '2023-06-07'),
	('17', 'admin', 'rex', 200, '2023-06-07'),
	('18', 'admin', '12', 522.5, '2023-06-07'),
	('19', 'admin', 'rex', 522.5, '2023-06-07'),
	('20', 'admin', 'hry', 522.5, '2023-06-07'),
	('21', 'admin', 'ret', 522.5, '2023-06-07'),
	('22', 'admin', 'rex', 1700, '2023-06-07'),
	('23', 'admin', 'rex', 30000, '2023-06-07'),
	('24', 'admin', 'rex', 500, '2023-06-07'),
	('25', 'admin', 'rex', 500, '2023-06-07'),
	('26', 'admin', 'rex', 1500, '2023-06-07'),
	('27', 'admin', 'rex', 500, '2023-06-07'),
	('28', 'admin', 'rex', 500, '2023-06-07'),
	('29', 'admin', 'rex', 522.5, '2023-06-07'),
	('30', 'admin', 'rex', 522.5, '2023-06-07'),
	('31', 'admin', 'rex', 500, '2023-06-07'),
	('32', 'admin', 'TJ', 13548.2, '2023-06-07'),
	('33', 'admin', 'rex', 1140.15, '2023-06-07'),
	('34', 'admin', 'Rexie', 1140.15, '2023-06-07'),
	('35', 'admin', 'rex', 522.5, '2023-06-08'),
	('36', 'admin', 'rex', 1500, '2023-06-08'),
	('37', 'admin', 'rex', 522.5, '2023-06-10');
/*!40000 ALTER TABLE `transaction_record` ENABLE KEYS */;

-- Dumping structure for table ssi.user_level_access
CREATE TABLE IF NOT EXISTS `user_level_access` (
  `Title` varchar(32) NOT NULL,
  `add_item` int(1) NOT NULL,
  PRIMARY KEY (`Title`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi.user_level_access: ~2 rows (approximately)
/*!40000 ALTER TABLE `user_level_access` DISABLE KEYS */;
INSERT INTO `user_level_access` (`Title`, `add_item`) VALUES
	('Assisstant', 0),
	('Owner', 1);
/*!40000 ALTER TABLE `user_level_access` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
