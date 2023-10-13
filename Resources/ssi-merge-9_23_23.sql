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


-- Dumping database structure for ssi_copy_1
CREATE DATABASE IF NOT EXISTS `ssi_copy_1` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `ssi_copy_1`;

-- Dumping structure for table ssi_copy_1.account_access_level
CREATE TABLE IF NOT EXISTS `account_access_level` (
  `usn` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
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
  PRIMARY KEY (`usn`) USING BTREE,
  KEY `usn` (`usn`) USING BTREE,
  CONSTRAINT `account_access_level_ibfk_1` FOREIGN KEY (`usn`) REFERENCES `acc_cred` (`usn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi_copy_1.account_access_level: ~8 rows (approximately)
INSERT INTO `account_access_level` (`usn`, `Dashboard`, `Reception`, `Payment`, `Services`, `Sales`, `Inventory`, `Pet_Info`, `Report`, `User`, `Action`, `Gen_Settings`) VALUES
	('123123', 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0),
	('admin', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
	('aila', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
	('assisstant', 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0),
	('Chris', 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0),
	('Chris2', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
	('Jrizal', 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0),
	('jayr', 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0);

-- Dumping structure for table ssi_copy_1.acc_cred
CREATE TABLE IF NOT EXISTS `acc_cred` (
  `usn` varchar(128) NOT NULL,
  `pss` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `slt` varchar(64) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `entry_OTP` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`usn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;

-- Dumping data for table ssi_copy_1.acc_cred: ~8 rows (approximately)
INSERT INTO `acc_cred` (`usn`, `pss`, `slt`, `entry_OTP`) VALUES
	('123123', '94bc6207156f186a77106c5c456a80017eff6f8d949265ecf515a4cb3b851eba', '3HCIZ_k8Speg-Ik3Ia2DgA==', NULL),
	('admin', '0c149295209d5f543cf1ba14956c5c135a78b9b311ad551715899e02c27dc99d', 'rCRF4amTSEOYQjqvWYuI7A==', NULL),
	('aila', 'b94fd2a2585dada0d309427f886092192a58ce549056edd56df595623b01cef9', 'ND08SurlSBKB74ch5HD9iQ==', NULL),
	('assisstant', '5362ca593f063f2581f756e9827bdd02da670bad2b176108380d7bc971ee5148', 'ljEGlbKwSZe3ECK-0b2K8g==', NULL),
	('Chris', 'f4de5587480de43270431146f49b462af3be91dade93e2550e236108b59804bf', 'VKxnK0f8T16nqO1xHdHMAg==', NULL),
	('Chris2', '8d01b6fcda79efa14555214d08d343e9e0496e7376800b2378bc8dc2d059e666', 'bzn1KLc2TwWxNQtgXooBBA==', NULL),
	('Jrizal', '4436a253401b8e74a80e7a9a04930e16ae6e37dbc8c36f49f871ead477044f53', '3wbtXJDmSTm98iubl13hLw==', NULL),
	('jayr', '56a1f73718b12d1a021f12eee52d2d1bbe1e6c067698c27e98c5fdd22fb0a0dd', 'WqMM26lyQDirax7evZgFuQ==', NULL);

-- Dumping structure for table ssi_copy_1.acc_info
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

-- Dumping data for table ssi_copy_1.acc_info: ~8 rows (approximately)
INSERT INTO `acc_info` (`usn`, `full_name`, `job_position`, `state`) VALUES
	('123123', '123123', 'Assisstant', 0),
	('admin', 'Big Boss 1', 'Owner', 1),
	('aila', 'aila', 'Assisstant', 1),
	('assisstant', 'Assisstant', 'Assisstant', 0),
	('Chris', 'Chris McLaind', 'Assisstant', 1),
	('Chris2', 'Chris2', 'Owner', 0),
	('Jrizal', 'Jose Rizal', 'Assisstant', 0),
	('jayr', 'jayr', 'Assisstant', 0);

-- Dumping structure for table ssi_copy_1.action_history
CREATE TABLE IF NOT EXISTS `action_history` (
  `Column 5` int(11) NOT NULL AUTO_INCREMENT,
  `usn` varchar(128) NOT NULL,
  `Type` varchar(25) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `ACTION` varchar(256) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `action_date` datetime NOT NULL,
  PRIMARY KEY (`Column 5`),
  KEY `usn` (`usn`),
  CONSTRAINT `action_history_ibfk_1` FOREIGN KEY (`usn`) REFERENCES `acc_cred` (`usn`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;

-- Dumping data for table ssi_copy_1.action_history: ~2 rows (approximately)
INSERT INTO `action_history` (`Column 5`, `usn`, `Type`, `ACTION`, `action_date`) VALUES
	(1, 'admin', 'Item Encoding', 'ADD/admin/I10fdf', '2023-09-11 23:50:11'),
	(2, 'aila', 'invoice', 'INVM/aila/Pec804', '2023-08-23 15:11:35');

-- Dumping structure for table ssi_copy_1.categories
CREATE TABLE IF NOT EXISTS `categories` (
  `categ_name` varchar(50) NOT NULL,
  `does_expire` int(1) DEFAULT NULL,
  PRIMARY KEY (`categ_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi_copy_1.categories: ~10 rows (approximately)
INSERT INTO `categories` (`categ_name`, `does_expire`) VALUES
	('Accessories', 0),
	('Food', 1),
	('Medicine', 1),
	('test', 0),
	('Test001', 1),
	('Test002', 0),
	('Test003', 0),
	('Test004', 1),
	('Test005', 1),
	('Test006', 0);

-- Dumping structure for table ssi_copy_1.disposal_history
CREATE TABLE IF NOT EXISTS `disposal_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `recieving_id` varchar(50) CHARACTER SET latin1 COLLATE latin1_general_cs DEFAULT NULL,
  `item_uid` varchar(6) NOT NULL,
  `item_name` varchar(64) NOT NULL,
  `Initial_quantity` int(11) DEFAULT NULL,
  `Current_quantity` int(11) NOT NULL,
  `reason` int(11) DEFAULT NULL,
  `date_of_disposal` datetime NOT NULL,
  `full_dispose_date` datetime DEFAULT NULL,
  `disposed_by` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `date_of_disposal` (`date_of_disposal`),
  UNIQUE KEY `full_dispose_date` (`full_dispose_date`),
  KEY `FK_disposal_history_recieving_item` (`recieving_id`),
  CONSTRAINT `FK_disposal_history_recieving_item` FOREIGN KEY (`recieving_id`) REFERENCES `recieving_item` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi_copy_1.disposal_history: ~9 rows (approximately)
INSERT INTO `disposal_history` (`id`, `recieving_id`, `item_uid`, `item_name`, `Initial_quantity`, `Current_quantity`, `reason`, `date_of_disposal`, `full_dispose_date`, `disposed_by`) VALUES
	(4, 'Ra9de5', 'I00002', 'Taglory Rope Dog Leash', 50, 50, NULL, '2023-08-30 21:53:12', '2023-08-30 23:10:34', 'admin'),
	(6, 'R86f29', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 15, 15, NULL, '2023-08-30 21:56:53', '2023-08-30 23:11:08', 'admin'),
	(7, 'R86f29', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 15, 15, NULL, '2023-08-30 22:03:02', NULL, 'admin'),
	(8, 'R86f29', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 15, 15, NULL, '2023-08-30 22:12:03', '2023-08-30 23:11:24', 'admin'),
	(9, 'R86f29', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 15, 15, NULL, '2023-08-30 22:13:15', '2023-08-30 23:11:14', 'admin'),
	(10, 'R31a74', 'I00003', 'Fresh Step Clumping Cat Litter', 5, 5, NULL, '2023-08-30 23:05:46', NULL, NULL),
	(11, 'R2ae83', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 5, 5, NULL, '2023-08-30 23:07:23', '2023-08-30 23:11:12', 'admin'),
	(12, 'Ra9de5', 'I00002', 'Taglory Rope Dog Leash', 50, 50, NULL, '2023-08-30 23:20:57', NULL, NULL),
	(13, 'Ra9de5', 'I00002', 'Taglory Rope Dog Leash', 50, 50, NULL, '2023-08-30 23:21:06', NULL, NULL);

-- Dumping structure for table ssi_copy_1.invoice_item_content
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

-- Dumping data for table ssi_copy_1.invoice_item_content: ~47 rows (approximately)
INSERT INTO `invoice_item_content` (`invoice_uid`, `Item_uid`, `item_name`, `quantity`, `price`, `deduction`) VALUES
	('Pc9c14', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('P2e8cf', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('P956ee', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('P22b46', 'I00002', 'Taglory Rope Dog Leash', 5, 440, 0),
	('P6953f', 'I00002', 'Taglory Rope Dog Leash', 2, 440, 0),
	('P660f0', 'I00002', 'Taglory Rope Dog Leash', 2, 440, 0),
	('P69823', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('P9754c', 'I00002', 'Taglory Rope Dog Leash', 3, 440, 0),
	('P4e070', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('P5d98a', 'I00002', 'Taglory Rope Dog Leash', 3, 440, 0),
	('P2792b', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('Pe327c', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('P15921', 'I00002', 'Taglory Rope Dog Leash', 4, 440, 0),
	('Pf6e9c', 'I00004', 'Fresh Step LeightWeight Clumping Cat ', 1, 796.95, 0),
	('Pec804', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('Pd260b', 'I00003', 'Fresh Step Clumping Cat Litter', 4, 577.5, 0),
	('P0ebe4', 'I00005', 'Nutri-Vet Bladder Control Supplement for Dogs', 2, 1140.15, 0),
	('P2cc66', 'I00003', 'Fresh Step Clumping Cat Litter', 1, 577.5, 0),
	('P2cc66', 'I00004', 'Fresh Step LeightWeight Clumping Cat Litter', 2, 796.95, 0),
	('08282302', 'I00005', 'Nutri-Vet Bladder Control Supplement for Dogs', 1, 1140.15, 0),
	('08282303', 'I00003', 'Fresh Step Clumping Cat Litter', 1, 577.5, 0),
	('08292300', 'I00003', 'Fresh Step Clumping Cat Litter', 1, 577.5, 0),
	('08292301', 'I00003', 'Fresh Step Clumping Cat Litter', 1, 577.5, 0),
	('08302314', 'I00003', 'Fresh Step Clumping Cat Litter', 1, 577.5, 0),
	('08302315', 'I00003', 'Fresh Step Clumping Cat Litter', 1, 577.5, 0),
	('08302316', 'I00003', 'Fresh Step Clumping Cat Litter', 4, 577.5, 0),
	('08302317', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('08302318', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 3, 522.5, 0),
	('08302319', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('08302320', 'I00003', 'Fresh Step Clumping Cat Litter', 1, 577.5, 0),
	('08312300', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 3, 522.5, 0),
	('08312301', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 2, 522.5, 0),
	('08312302', 'I00002', 'Taglory Rope Dog Leash', 2, 440, 0),
	('08312303', 'I00003', 'Fresh Step Clumping Cat Litter', 2, 577.5, 0),
	('08312304', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('08312305', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('08312306', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 3, 522.5, 0),
	('08312307', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('08312308', 'I00004', 'Fresh Step LeightWeight Clumping Cat Litter', 3, 796.95, 0),
	('08312309', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('08312310', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 3, 522.5, 0),
	('08312311', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 3, 522.5, 0),
	('09022300', 'I00005', 'Nutri-Vet Bladder Control Supplement for Dogs', 2, 1140.15, 0),
	('09032309', 'I00005', 'Nutri-Vet Bladder Control Supplement for Dogs', 2, 1140.15, 0),
	('09032310', 'I00005', 'Nutri-Vet Bladder Control Supplement for Dogs', 2, 1140.15, 0),
	('09032311', 'I00006', 'UniLeash', 2, 144, 0),
	('23092200', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0);

-- Dumping structure for table ssi_copy_1.invoice_record
CREATE TABLE IF NOT EXISTS `invoice_record` (
  `invoice_uid` varchar(8) NOT NULL,
  `Attendant_usn` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
  `client_name` varchar(50) NOT NULL,
  `Total_amount` float NOT NULL,
  `payment_date` datetime DEFAULT NULL,
  `transaction_date` date NOT NULL,
  `State` int(1) NOT NULL DEFAULT 0,
  `Date_transacted` date DEFAULT NULL,
  PRIMARY KEY (`invoice_uid`),
  KEY `Attendant_usn` (`Attendant_usn`) USING BTREE,
  CONSTRAINT `invoice_record_ibfk_1` FOREIGN KEY (`Attendant_usn`) REFERENCES `acc_cred` (`usn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi_copy_1.invoice_record: ~96 rows (approximately)
INSERT INTO `invoice_record` (`invoice_uid`, `Attendant_usn`, `client_name`, `Total_amount`, `payment_date`, `transaction_date`, `State`, `Date_transacted`) VALUES
	('08282302', 'aila', 'N/A', 1140.15, NULL, '2023-08-28', -1, NULL),
	('08282303', 'aila', 'N/A', 577.5, NULL, '2023-08-28', 2, '2023-08-29'),
	('08292300', 'aila', 'N/A', 577.5, NULL, '2023-08-29', -1, NULL),
	('08292301', 'aila', 'N/A', 577.5, NULL, '2023-08-29', 2, '2023-08-30'),
	('08292302', 'aila', 'Bud Tan', 500, NULL, '2023-08-29', 2, '2023-08-29'),
	('08292303', 'aila', 'Bud Tan', 900, NULL, '2023-08-29', -1, NULL),
	('08292304', 'aila', 'Bud Tan', 500, NULL, '2023-08-29', 2, '2023-08-29'),
	('08292305', 'aila', 'Bud Tan', 500, NULL, '2023-08-29', 2, '2023-08-29'),
	('08292306', 'aila', 'Bud Tan', 1500, NULL, '2023-08-29', 2, '2023-08-29'),
	('08292307', 'aila', 'Bud Tan', 500, NULL, '2023-08-29', -1, NULL),
	('08292308', 'aila', 'James V.', 500, NULL, '2023-08-29', 2, '2023-08-29'),
	('08292309', 'aila', 'Bud Tan', 500, NULL, '2023-08-29', -1, NULL),
	('08292310', 'aila', 'Jose R.', 1700, NULL, '2023-08-29', 2, '2023-08-29'),
	('08302300', 'aila', 'James V.', 500, NULL, '2023-08-30', 2, '2023-08-30'),
	('08302301', 'aila', 'James V.', 1500, NULL, '2023-08-30', -1, NULL),
	('08302302', 'aila', 'James V.', 3000, NULL, '2023-08-30', 2, '2023-08-30'),
	('08302303', 'aila', 'Bud Tan', 2100, NULL, '2023-08-30', 2, '2023-08-30'),
	('08302304', 'aila', 'James V.', 900, NULL, '2023-08-30', -1, NULL),
	('08302305', 'aila', 'Bud Tan', 500, NULL, '2023-08-30', 2, '2023-08-30'),
	('08302306', 'aila', 'Bud Tan', 500, NULL, '2023-08-30', 2, '2023-08-30'),
	('08302307', 'aila', 'Bud Tan', 500, NULL, '2023-08-30', 2, '2023-08-30'),
	('08302308', 'aila', 'James V.', 500, NULL, '2023-08-30', -1, NULL),
	('08302309', 'aila', 'James V.', 1000, NULL, '2023-08-30', -1, NULL),
	('08302310', 'aila', 'James V.', 1000, NULL, '2023-08-30', -1, NULL),
	('08302311', 'aila', 'James V.', 1500, NULL, '2023-08-30', -1, NULL),
	('08302312', 'aila', 'James V.', 1000, NULL, '2023-08-30', -1, NULL),
	('08302313', 'aila', 'James V.', 500, NULL, '2023-08-30', 2, '2023-08-30'),
	('08302314', 'aila', 'N/A', 577.5, NULL, '2023-08-30', 2, '2023-08-30'),
	('08302315', 'aila', 'N/A', 577.5, NULL, '2023-08-30', 2, '2023-08-30'),
	('08302316', 'admin', 'Christopher L.', 2310, NULL, '2023-08-30', 2, '2023-08-30'),
	('08302317', 'admin', 'N/A', 522.5, NULL, '2023-08-30', 2, '2023-08-30'),
	('08302318', 'admin', 'James V.', 1567.5, NULL, '2023-08-30', 2, '2023-08-30'),
	('08302319', 'admin', 'N/A', 522.5, NULL, '2023-08-30', 2, '2023-08-30'),
	('08302320', 'admin', 'N/A', 577.5, NULL, '2023-08-30', 2, '2023-08-30'),
	('08312300', 'admin', 'Bud Tan', 1567.5, NULL, '2023-08-31', 2, '2023-08-31'),
	('08312301', 'admin', 'N/A', 1045, NULL, '2023-08-31', 2, '2023-08-31'),
	('08312302', 'admin', 'N/A', 880, NULL, '2023-08-31', 2, '2023-08-31'),
	('08312303', 'admin', 'N/A', 1155, NULL, '2023-08-31', 2, '2023-08-31'),
	('08312304', 'admin', 'N/A', 522.5, NULL, '2023-08-31', 2, '2023-08-31'),
	('08312305', 'admin', 'N/A', 522.5, NULL, '2023-08-31', 2, '2023-08-31'),
	('08312306', 'admin', 'N/A', 1567.5, NULL, '2023-08-31', 2, '2023-08-31'),
	('08312307', 'admin', 'N/A', 522.5, NULL, '2023-08-31', 2, '2023-09-02'),
	('08312308', 'admin', 'N/A', 2390.85, NULL, '2023-08-31', 2, '2023-08-31'),
	('08312309', 'admin', 'N/A', 522.5, NULL, '2023-08-31', 2, '2023-08-31'),
	('08312310', 'admin', 'N/A', 1567.5, NULL, '2023-08-31', 2, '2023-08-31'),
	('08312311', 'admin', 'N/A', 1567.5, NULL, '2023-08-31', 2, '2023-08-31'),
	('09022300', 'admin', 'James V.', 2780.3, NULL, '2023-09-02', 2, '2023-09-02'),
	('09022301', 'admin', 'James V.', 1000, NULL, '2023-09-02', 2, '2023-09-03'),
	('09022302', 'admin', 'Davin F.', 2500, NULL, '2023-09-02', 2, '2023-09-03'),
	('09022303', 'admin', 'Bud Tan', 500, NULL, '2023-09-02', 2, '2023-09-02'),
	('09022304', 'admin', 'Jose R.', 1000, NULL, '2023-09-02', 2, '2023-09-03'),
	('09022305', 'admin', 'James V.', 500, NULL, '2023-09-02', 2, '2023-09-03'),
	('09022306', 'admin', 'Patrick Feniza', 500, NULL, '2023-09-02', 2, '2023-09-02'),
	('09032300', 'admin', 'Patrick Feniza', 500, NULL, '2023-09-03', 2, '2023-09-03'),
	('09032301', 'admin', 'Bud Tan', 500, NULL, '2023-09-03', 2, '2023-09-03'),
	('09032302', 'admin', 'Patrick Feniza', 500, NULL, '2023-09-03', 2, '2023-09-03'),
	('09032303', 'admin', 'Patrick Feniza', 2500, NULL, '2023-09-03', 2, '2023-09-03'),
	('09032304', 'admin', 'James V.', 3000, NULL, '2023-09-03', 2, '2023-09-03'),
	('09032305', 'admin', 'Davin F.', 4600, NULL, '2023-09-03', 2, '2023-09-03'),
	('09032306', 'admin', 'James V.', 2100, NULL, '2023-09-03', 2, '2023-09-03'),
	('09032307', 'admin', 'Patrick Feniza', 2000, NULL, '2023-09-03', 2, '2023-09-03'),
	('09032308', 'admin', 'Christopher L.', 2500, NULL, '2023-09-03', 2, '2023-09-03'),
	('09032309', 'admin', 'N/A', 2280.3, NULL, '2023-09-03', 2, '2023-09-03'),
	('09032310', 'admin', 'N/A', 2280.3, NULL, '2023-09-03', 2, '2023-09-03'),
	('09032311', 'admin', 'N/A', 288, NULL, '2023-09-03', 2, '2023-09-03'),
	('09032312', 'admin', 'Patrick Feniza', 500, NULL, '2023-09-03', 1, NULL),
	('09032313', 'admin', 'Patrick Feniza', 1500, NULL, '2023-09-03', -1, NULL),
	('09072300', 'admin', 'Patrick Feniza', 500, NULL, '2023-09-07', -1, NULL),
	('09072301', 'admin', 'James Viñas', 4500, NULL, '2023-09-07', 2, '2023-09-07'),
	('09082300', 'admin', 'Budjette Tan', 500, NULL, '2023-09-08', 1, NULL),
	('23092200', 'admin', 'N/A', 0, '2023-09-22 11:18:44', '2023-09-22', 1, NULL),
	('P0b8cb', 'aila', 'James V.', 2100, NULL, '2023-08-26', -1, NULL),
	('P0e4d2', 'aila', 'James V.', 500, NULL, '2023-08-20', 2, '2023-08-22'),
	('P0ebe4', 'aila', 'James V.', 2280.3, NULL, '2023-08-26', 2, '2023-08-26'),
	('P14b84', 'aila', 'Jose R.', 0, NULL, '2023-08-26', 2, '2023-08-30'),
	('P15921', 'aila', 'N/A', 1760, NULL, '2023-08-23', 2, '2023-08-23'),
	('P1d58d', 'aila', 'James V.', 500, NULL, '2023-08-19', 2, '2023-08-20'),
	('P22b46', 'aila', 'N/A', 2200, NULL, '2023-08-20', 2, '2023-08-22'),
	('P2792b', 'aila', 'N/A', 440, NULL, '2023-08-22', 2, '2023-08-22'),
	('P2cc66', 'aila', 'N/A', 2171.4, NULL, '2023-08-28', 2, '2023-08-28'),
	('P2e8cf', 'aila', 'N/A', 440, NULL, '2023-08-19', 2, '2023-08-22'),
	('P31f82', 'aila', 'N/A', 0, NULL, '2023-08-28', -1, NULL),
	('P3d236', 'aila', 'Davin F.', 500, NULL, '2023-08-19', 2, '2023-08-22'),
	('P4e070', 'aila', 'N/A', 440, NULL, '2023-08-22', 2, '2023-08-22'),
	('P5a62c', 'aila', 'Davin F.', 500, NULL, '2023-08-28', 2, '2023-08-29'),
	('P5d98a', 'aila', 'N/A', 1320, NULL, '2023-08-22', 2, '2023-08-22'),
	('P660f0', 'aila', 'N/A', 880, NULL, '2023-08-20', 2, '2023-08-20'),
	('P6848e', 'aila', 'James V.', 2100, NULL, '2023-08-26', -1, NULL),
	('P6953f', 'aila', 'James V.', 1380, NULL, '2023-08-20', 2, '2023-08-20'),
	('P69823', 'aila', 'N/A', 440, NULL, '2023-08-22', 2, '2023-08-22'),
	('P956ee', 'aila', 'N/A', 440, NULL, '2023-08-19', 2, '2023-08-22'),
	('P9754c', 'aila', 'N/A', 1320, NULL, '2023-08-22', 2, '2023-08-22'),
	('Pc0aa9', 'aila', 'James V.', 1500, NULL, '2023-08-20', 2, '2023-08-20'),
	('Pc7cae', 'aila', 'Jose R.', 0, NULL, '2023-08-26', 2, '2023-08-28'),
	('Pc9c14', 'aila', 'N/A', 440, NULL, '2023-08-19', 2, '2023-08-22'),
	('Pd260b', 'aila', 'N/A', 2310, NULL, '2023-08-23', 2, '2023-08-28'),
	('Pe327c', 'aila', 'Jose R.', 440, NULL, '2023-08-23', 2, '2023-08-23'),
	('Pec804', 'aila', 'Christopher L.', 440, NULL, '2023-08-23', -1, NULL),
	('Pf6e9c', 'aila', 'N/A', 796.95, NULL, '2023-08-23', 2, '2023-08-23');

-- Dumping structure for table ssi_copy_1.invoice_service_content
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

-- Dumping data for table ssi_copy_1.invoice_service_content: ~58 rows (approximately)
INSERT INTO `invoice_service_content` (`invoice_uid`, `service_uid`, `service_name`, `pet_uid`, `patient_name`, `scheduled_date`, `price`, `deduction`, `end_schedule`, `multiple_sched_quan`, `instance_of_mul_sched`) VALUES
	('P1d58d', 'S00001', 'Grooming', 'P1ec18', 'Brutus', '2023-08-19', 500, 0, NULL, NULL, NULL),
	('P3d236', 'S00001', 'Grooming', 'P536ec', 'Clarence', '2023-08-19', 500, 0, NULL, NULL, NULL),
	('P6953f', 'S00001', 'Grooming', 'P1ec18', 'Brutus', '2023-08-20', 500, 0, NULL, NULL, NULL),
	('P0e4d2', 'S00001', 'Grooming', 'P1ec18', 'Brutus', '2023-08-20', 500, 0, NULL, NULL, NULL),
	('Pc0aa9', 'S00002', '5-in-1 Vaccine', 'P1ec18', 'Brutus', '2023-08-20', 1500, 0, NULL, NULL, NULL),
	('P5a62c', 'S00001', 'Grooming', '143436', 'Gabi', '2023-08-28', 500, 0, NULL, NULL, NULL),
	('08292302', 'S00001', 'Grooming', '012633', 'Bantay', '2023-08-29', 500, 0, NULL, NULL, NULL),
	('08292304', 'S00001', 'Grooming', '012633', 'Bantay', '2023-08-29', 500, 0, NULL, NULL, NULL),
	('08292305', 'S00001', 'Grooming', '012633', 'Bantay', '2023-08-29', 500, 0, NULL, NULL, NULL),
	('08292306', 'S00002', '5-in-1 Vaccine', '012633', 'Bantay', '2023-08-29', 1500, 0, NULL, NULL, NULL),
	('08292308', 'S00001', 'Grooming', '015659', 'Ruko', '2023-08-29', 500, 0, NULL, NULL, NULL),
	('08292309', 'S00001', 'Grooming', '012633', 'Bantay', '2023-08-31', 500, 0, NULL, NULL, NULL),
	('08292310', 'S00005', 'Canine Castration Surgery', 'P482dc', 'Whitey', '2023-08-30', 1700, 0, NULL, NULL, NULL),
	('08302300', 'S00001', 'Grooming', '015659', 'Ruko', '2023-08-31', 500, 0, NULL, NULL, NULL),
	('08302302', 'S00002', '5-in-1 Vaccine', '015659', 'Ruko', '2023-09-08', 1500, 0, NULL, NULL, NULL),
	('08302302', 'S00002', '5-in-1 Vaccine', 'P1ec18', 'Brutus', '2023-09-09', 1500, 0, NULL, NULL, NULL),
	('08302303', 'S00004', 'Yeast Infection Treatment', '012633', 'Bantay', '2023-08-31', 2100, 0, NULL, NULL, NULL),
	('08302306', 'S00001', 'Grooming', '012633', 'Bantay', '2023-08-31', 500, 0, NULL, NULL, NULL),
	('08302307', 'S00001', 'Grooming', '012633', 'Bantay', '2023-08-30', 500, 0, NULL, NULL, NULL),
	('08302308', 'S00001', 'Grooming', '015659', 'Ruko', '2023-08-30', 500, 0, NULL, NULL, NULL),
	('08302308', 'S00001', 'Grooming', 'P1ec18', 'Brutus', '2023-08-31', 500, 0, NULL, NULL, NULL),
	('08302309', 'S00001', 'Grooming', '015659', 'Ruko', '2023-08-31', 500, 0, NULL, NULL, NULL),
	('08302309', 'S00001', 'Grooming', 'P1ec18', 'Brutus', '2023-08-31', 500, 0, NULL, NULL, NULL),
	('08302310', 'S00001', 'Grooming', '015659', 'Ruko', '2023-08-31', 500, 0, NULL, NULL, NULL),
	('08302310', 'S00001', 'Grooming', 'P1ec18', 'Brutus', '2023-09-28', 500, 0, NULL, NULL, NULL),
	('08302311', 'S00002', '5-in-1 Vaccine', '015659', 'Ruko', '2023-09-28', 1500, 0, NULL, NULL, NULL),
	('08302311', 'S00002', '5-in-1 Vaccine', 'P1ec18', 'Brutus', '2023-08-31', 1500, 0, NULL, NULL, NULL),
	('08302312', 'S00001', 'Grooming', '015659', 'Ruko', '2023-08-30', 500, 0, NULL, NULL, NULL),
	('08302312', 'S00001', 'Grooming', 'P1ec18', 'Brutus', '2023-09-28', 500, 0, NULL, NULL, NULL),
	('08302313', 'S00001', 'Grooming', '015659', 'Ruko', '2023-08-31', 500, 0, NULL, NULL, NULL),
	('09022300', 'S00001', 'Grooming', 'P1ec18', 'Brutus', '2023-09-02', 500, 0, NULL, NULL, NULL),
	('09022301', 'S00001', 'Grooming', '015659', 'Ruko', '2023-09-02', 500, 0, NULL, NULL, NULL),
	('09022301', 'S00001', 'Grooming', 'P1ec18', 'Brutus', '2023-09-02', 500, 0, NULL, NULL, NULL),
	('09022302', 'S00003', 'Papiloma Vaccine', '143436', 'Gabi', '2023-09-02', 2500, 0, NULL, NULL, NULL),
	('09022303', 'S00001', 'Grooming', '012633', 'Bantay', '2023-09-02', 500, 0, NULL, NULL, NULL),
	('09022304', 'S00001', 'Grooming', 'P6b73f', 'Browny', '2023-09-02', 500, 0, NULL, NULL, NULL),
	('09022304', 'S00001', 'Grooming', 'P482dc', 'Whitey', '2023-09-08', 500, 0, NULL, NULL, NULL),
	('09022305', 'S00001', 'Grooming', '015659', 'Ruko', '2023-09-03', 500, 0, NULL, NULL, NULL),
	('09022306', 'S00001', 'Grooming', '234905', 'TJ', '2023-09-02', 500, 0, NULL, NULL, NULL),
	('09032300', 'S00001', 'Grooming', '234905', 'TJ', '2023-09-03', 500, 0, NULL, NULL, NULL),
	('09032301', 'S00001', 'Grooming', '012633', 'Bantay', '2023-09-03', 500, 0, NULL, NULL, NULL),
	('09032302', 'S00001', 'Grooming', '001431', 'Muning', '2023-09-03', 500, 0, NULL, NULL, NULL),
	('09032303', 'S00003', 'Papiloma Vaccine', '001431', 'Muning', '2023-09-03', 2500, 0, NULL, NULL, NULL),
	('09032304', 'S00001', 'Grooming', '015659', 'Ruko', '2023-09-03', 500, 0, NULL, NULL, NULL),
	('09032304', 'S00003', 'Papiloma Vaccine', '015659', 'Ruko', '2023-09-03', 2500, 0, NULL, NULL, NULL),
	('09032305', 'S00004', 'Yeast Infection Treatment', 'P536ec', 'Clarence', '2023-09-03', 2100, 0, NULL, NULL, NULL),
	('09032305', 'S00003', 'Papiloma Vaccine', 'P536ec', 'Clarence', '2023-09-03', 2500, 0, NULL, NULL, NULL),
	('09032306', 'S00004', 'Yeast Infection Treatment', '234729', 'Miru', '2023-09-03', 2100, 0, NULL, NULL, NULL),
	('09032307', 'S00001', 'Grooming', '234905', 'TJ', '2023-09-03', 500, 0, NULL, NULL, NULL),
	('09032307', 'S00002', '5-in-1 Vaccine', '234905', 'TJ', '2023-09-03', 1500, 0, NULL, NULL, NULL),
	('09032308', 'S00003', 'Papiloma Vaccine', 'Pb6c0b', 'Luna', '2023-09-03', 2500, 0, NULL, NULL, NULL),
	('09032312', 'S00001', 'Grooming', '001431', 'Muning', '2023-09-03', 500, 0, NULL, NULL, NULL),
	('09032313', 'S00002', '5-in-1 Vaccine', '234905', 'TJ', '2023-09-03', 1500, 0, NULL, NULL, NULL),
	('09072300', 'S00001', 'Grooming', '001431', 'Muning', '2023-09-07', 500, 0, NULL, NULL, NULL),
	('09072301', 'S00002', '5-in-1 Vaccine', '015659', 'Ruko', '2023-09-07', 1500, 0, NULL, NULL, NULL),
	('09072301', 'S00002', '5-in-1 Vaccine', 'P1ec18', 'Brutus', '2023-09-07', 1500, 0, NULL, NULL, NULL),
	('09072301', 'S00002', '5-in-1 Vaccine', '015659', 'Ruko', '2023-09-07', 1500, 0, NULL, NULL, NULL),
	('09082300', 'S00001', 'Grooming', '012633', 'Bantay', '2023-09-08', 500, 0, NULL, NULL, NULL);

-- Dumping structure for table ssi_copy_1.item_general_info
CREATE TABLE IF NOT EXISTS `item_general_info` (
  `UID` varchar(6) NOT NULL,
  `name` varchar(64) NOT NULL,
  `Category` varchar(64) NOT NULL,
  PRIMARY KEY (`UID`),
  UNIQUE KEY `name` (`name`),
  KEY `Category` (`Category`),
  CONSTRAINT `item_general_info_ibfk_1` FOREIGN KEY (`Category`) REFERENCES `categories` (`categ_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi_copy_1.item_general_info: ~16 rows (approximately)
INSERT INTO `item_general_info` (`UID`, `name`, `Category`) VALUES
	('I00001', 'MayPaw Heavy Duty Rope Dog Leash', 'Accessories'),
	('I00002', 'Taglory Rope Dog Leash', 'Accessories'),
	('I00003', 'Fresh Step Clumping Cat Litter', 'Accessories'),
	('I00004', 'Fresh Step LeightWeight Clumping Cat Litter', 'Accessories'),
	('I00005', 'Nutri-Vet Bladder Control Supplement for Dogs', 'Medicine'),
	('I00006', 'UniLeash', 'Accessories'),
	('I00007', 'Amoxiccilin Paracetamol 250mg', 'Medicine'),
	('I0AE71', 'Test ITem 003', 'Accessories'),
	('I10fdf', 'Test', 'Accessories'),
	('I1aa81', 'Comedy', 'Accessories'),
	('I2b993', 'Kessoku Band', 'Accessories'),
	('I39DC8', 'Test Item 002', 'Accessories'),
	('I7A986', 'TEST ITEM 004', 'Accessories'),
	('Ia71e7', 'Kawaki wo ameku', 'Accessories'),
	('Iaad08', 'Test Item', 'Accessories'),
	('IACBE3', 'Test Item 006', 'Test003'),
	('IFF357', 'Test Item 005', 'Accessories');

-- Dumping structure for table ssi_copy_1.item_inventory_info
CREATE TABLE IF NOT EXISTS `item_inventory_info` (
  `UID` varchar(6) NOT NULL,
  `Stock` int(11) NOT NULL,
  `Expiry_Date` date DEFAULT NULL,
  `state` int(1) NOT NULL DEFAULT 1,
  KEY `UID` (`UID`),
  CONSTRAINT `item_inventory_info_ibfk_1` FOREIGN KEY (`UID`) REFERENCES `item_general_info` (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi_copy_1.item_inventory_info: ~29 rows (approximately)
INSERT INTO `item_inventory_info` (`UID`, `Stock`, `Expiry_Date`, `state`) VALUES
	('I00002', -2, NULL, 1),
	('I00003', 49, NULL, 1),
	('I00004', 46, NULL, 1),
	('I00005', 114, '2023-10-26', 1),
	('I00005', 45, '2023-08-31', -1),
	('I00006', 207, NULL, 1),
	('I00005', 10, NULL, 1),
	('I00005', -1, NULL, 1),
	('I00005', 35, NULL, 1),
	('I00001', 39, NULL, 1),
	('I00003', 2, NULL, 1),
	('I00001', -1, NULL, 1),
	('I00005', 1, '2023-09-28', 1),
	('I00004', 5, NULL, 1),
	('I00004', 3, NULL, 1),
	('I00004', 3, NULL, 1),
	('I00002', 8, NULL, 1),
	('I1aa81', 10, NULL, 1),
	('Ia71e7', 110, NULL, 1),
	('I2b993', 0, NULL, 1),
	('Iaad08', 110, NULL, 1),
	('I39DC8', 10, NULL, 1),
	('I0AE71', 50, NULL, 1),
	('I7A986', 10, NULL, 1),
	('IFF357', 10, NULL, 1),
	('IACBE3', 10, NULL, 1);

-- Dumping structure for table ssi_copy_1.item_settings
CREATE TABLE IF NOT EXISTS `item_settings` (
  `UID` varchar(6) NOT NULL,
  `Cost_Price` float NOT NULL,
  `Markup_Factor` float NOT NULL,
  `Reorder_factor` float NOT NULL,
  `Crit_factor` float NOT NULL,
  `Safe_stock` int(11) NOT NULL,
  `Average_monthly_selling_rate` int(11) NOT NULL,
  PRIMARY KEY (`UID`),
  CONSTRAINT `item_settings_ibfk_1` FOREIGN KEY (`UID`) REFERENCES `item_general_info` (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi_copy_1.item_settings: ~14 rows (approximately)
INSERT INTO `item_settings` (`UID`, `Cost_Price`, `Markup_Factor`, `Reorder_factor`, `Crit_factor`, `Safe_stock`, `Average_monthly_selling_rate`) VALUES
	('I00001', 475, 0.1, 0.85, 0.5, 50, 5),
	('I00002', 400, 0.1, 0.85, 0.5, 50, 5),
	('I00003', 525, 0.1, 0.85, 0.5, 25, 5),
	('I00004', 724.5, 0.1, 0.85, 0.5, 25, 5),
	('I00005', 1036.5, 0.1, 0.85, 0.5, 85, 5),
	('I00006', 120, 0.2, 0.75, 0.5, 15, 5),
	('I0AE71', 100, 2.1, 0.85, 0.5, 10, 5),
	('I10fdf', 100, 0, 0.85, 0.5, 50, 5),
	('I1aa81', 123, 0.9709, 0.85, 0.5, 8, 5),
	('I2b993', 121, 0.9901, 0.85, 0.5, 5, 5),
	('I39DC8', 100, 0.1, 0.85, 0.5, 10, 5),
	('I7A986', 1000, 0.01, 0.85, 0.5, 10, 5),
	('Ia71e7', 123, 0.9901, 0.85, 0.5, 55, 5),
	('Iaad08', 100, 0.1, 0.85, 0.5, 100, 5),
	('IACBE3', 100, 0.01, 0.85, 0.5, 10, 5),
	('IFF357', 100, 0.1, 0.85, 0.5, 10, 5);

-- Dumping structure for table ssi_copy_1.item_supplier_info
CREATE TABLE IF NOT EXISTS `item_supplier_info` (
  `UID` varchar(6) NOT NULL,
  `supp_id` varchar(8) NOT NULL,
  PRIMARY KEY (`UID`),
  KEY `supplier_info_fk` (`supp_id`) USING BTREE,
  CONSTRAINT `FK_item_supplier_info_supplier_info` FOREIGN KEY (`supp_id`) REFERENCES `supplier_info` (`supp_id`),
  CONSTRAINT `item_supplier_info_ibfk_1` FOREIGN KEY (`UID`) REFERENCES `item_general_info` (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi_copy_1.item_supplier_info: ~17 rows (approximately)
INSERT INTO `item_supplier_info` (`UID`, `supp_id`) VALUES
	('I0AE71', 'SU000001'),
	('I39DC8', 'SU000001'),
	('IACBE3', 'SU000001'),
	('IFF357', 'SU000001'),
	('I7A986', 'SU000002'),
	('I00003', 'SU000003'),
	('I1aa81', 'SU000003'),
	('I00001', 'SU000004'),
	('I00002', 'SU000004'),
	('I00004', 'SU000004'),
	('I00005', 'SU000004'),
	('I00006', 'SU000004'),
	('I10fdf', 'SU000004'),
	('I2b993', 'SU000004'),
	('I00007', 'SU000005'),
	('Ia71e7', 'SU000005'),
	('Iaad08', 'SU000005');

-- Dumping structure for table ssi_copy_1.item_transaction_content
CREATE TABLE IF NOT EXISTS `item_transaction_content` (
  `transaction_uid` varchar(8) NOT NULL,
  `Item_uid` varchar(6) NOT NULL,
  `item_name` varchar(64) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` float NOT NULL,
  `deduction` float NOT NULL,
  KEY `FK_item_transaction_content_transaction_record` (`transaction_uid`),
  CONSTRAINT `FK_item_transaction_content_transaction_record` FOREIGN KEY (`transaction_uid`) REFERENCES `transaction_record` (`transaction_uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi_copy_1.item_transaction_content: ~50 rows (approximately)
INSERT INTO `item_transaction_content` (`transaction_uid`, `Item_uid`, `item_name`, `quantity`, `price`, `deduction`) VALUES
	('0', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 2, 522.5, 0),
	('2', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('3', 'I00005', 'Nutri-Vet Bladder Control Supplement for Dogs', 3, 1140.15, 0),
	('6', 'I00004', 'Fresh Step LeightWeight Clumping Cat Litter', 4, 796.95, 0),
	('8', 'I00004', 'Fresh Step LeightWeight Clumping Cat Litter', 2, 796.95, 0),
	('9', 'I00006', 'UniLeash', 1, 144, 0),
	('11', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('14', 'I00002', 'Taglory Rope Dog Leash', 3, 440, 0),
	('15', 'I00002', 'Taglory Rope Dog Leash', 2, 440, 0),
	('16', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('16', 'I00004', 'Fresh Step LeightWeight Clumping Cat Litter', 2, 796.95, 0),
	('17', 'I00002', 'Taglory Rope Dog Leash', 2, 880, 0),
	('19', 'I00002', 'Taglory Rope Dog Leash', 2, 880, 0),
	('23', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('25', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('26', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('27', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('29', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('31', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('33', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('34', 'I00004', 'Fresh Step LeightWeight Clumping Cat ', 1, 796.95, 0),
	('36', 'I00003', 'Fresh Step Clumping Cat Litter', 4, 577.5, 0),
	('37', 'I00003', 'Fresh Step Clumping Cat Litter', 1, 577.5, 0),
	('37', 'I00004', 'Fresh Step LeightWeight Clumping Cat Litter', 2, 796.95, 0),
	('39', 'I00003', 'Fresh Step Clumping Cat Litter', 1, 577.5, 0),
	('43', 'I00003', 'Fresh Step Clumping Cat Litter', 1, 577.5, 0),
	('46', 'I00003', 'Fresh Step Clumping Cat Litter', 1, 577.5, 0),
	('47', 'I00003', 'Fresh Step Clumping Cat Litter', 1, 577.5, 0),
	('48', 'I00003', 'Fresh Step Clumping Cat Litter', 4, 577.5, 0),
	('49', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('50', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 3, 522.5, 0),
	('50', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('51', 'I00003', 'Fresh Step Clumping Cat Litter', 1, 577.5, 0),
	('52', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 3, 522.5, 0),
	('52', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 3, 522.5, 0),
	('52', 'I00002', 'Taglory Rope Dog Leash', 2, 440, 0),
	('53', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 2, 522.5, 0),
	('54', 'I00003', 'Fresh Step Clumping Cat Litter', 2, 577.5, 0),
	('55', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('56', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('56', 'I00004', 'Fresh Step LeightWeight Clumping Cat Litter', 3, 796.95, 0),
	('56', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 3, 522.5, 0),
	('57', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('58', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 3, 522.5, 0),
	('58', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 3, 522.5, 0),
	('59', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('60', 'I00005', 'Nutri-Vet Bladder Control Supplement for Dogs', 2, 1140.15, 0),
	('75', 'I00005', 'Nutri-Vet Bladder Control Supplement for Dogs', 2, 1140.15, 0),
	('76', 'I00005', 'Nutri-Vet Bladder Control Supplement for Dogs', 2, 1140.15, 0),
	('77', 'I00006', 'UniLeash', 2, 144, 0);

-- Dumping structure for table ssi_copy_1.login_report
CREATE TABLE IF NOT EXISTS `login_report` (
  `attempt_usn` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_cs DEFAULT NULL,
  `usn_used` varchar(128) NOT NULL,
  `date_created` datetime NOT NULL,
  KEY `attempt_usn` (`attempt_usn`),
  CONSTRAINT `login_report_ibfk_1` FOREIGN KEY (`attempt_usn`) REFERENCES `acc_cred` (`usn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi_copy_1.login_report: ~4 rows (approximately)
INSERT INTO `login_report` (`attempt_usn`, `usn_used`, `date_created`) VALUES
	(NULL, 'admin', '2023-06-07 23:50:59'),
	('admin', 'admin', '2023-06-07 23:54:09'),
	('admin', 'admin', '2023-06-07 23:55:45'),
	(NULL, 'chris', '2023-07-05 17:36:56');

-- Dumping structure for table ssi_copy_1.log_history
CREATE TABLE IF NOT EXISTS `log_history` (
  `usn` varchar(128) NOT NULL,
  `date_logged` date NOT NULL,
  `time_in` time NOT NULL,
  `time_out` time NOT NULL,
  KEY `usn` (`usn`),
  CONSTRAINT `log_history_ibfk_1` FOREIGN KEY (`usn`) REFERENCES `acc_cred` (`usn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;

-- Dumping data for table ssi_copy_1.log_history: ~31 rows (approximately)
INSERT INTO `log_history` (`usn`, `date_logged`, `time_in`, `time_out`) VALUES
	('Chris2', '2023-08-31', '00:05:36', '00:05:36'),
	('admin', '2023-09-11', '23:28:25', '23:28:25'),
	('admin', '2023-09-12', '14:20:59', '14:20:59'),
	('admin', '2023-09-12', '15:57:56', '15:57:56'),
	('admin', '2023-09-12', '15:59:58', '15:59:58'),
	('admin', '2023-09-12', '16:04:04', '16:04:04'),
	('admin', '2023-09-12', '16:06:23', '16:06:23'),
	('admin', '2023-09-12', '16:07:52', '16:07:52'),
	('admin', '2023-09-12', '16:09:02', '16:09:02'),
	('admin', '2023-09-12', '16:09:45', '16:09:45'),
	('admin', '2023-09-12', '16:10:40', '16:10:40'),
	('admin', '2023-09-12', '16:12:07', '16:12:07'),
	('admin', '2023-09-12', '16:14:13', '16:14:13'),
	('admin', '2023-09-12', '16:23:08', '16:23:08'),
	('admin', '2023-09-12', '16:24:11', '16:24:11'),
	('admin', '2023-09-12', '16:25:26', '16:25:26'),
	('admin', '2023-09-12', '16:26:01', '16:26:01'),
	('admin', '2023-09-12', '16:27:41', '16:27:41'),
	('admin', '2023-09-12', '16:29:48', '16:29:48'),
	('admin', '2023-09-12', '16:30:52', '16:30:52'),
	('admin', '2023-09-12', '16:36:18', '16:36:18'),
	('admin', '2023-09-12', '16:37:16', '16:37:16'),
	('admin', '2023-09-12', '16:49:22', '16:49:22'),
	('admin', '2023-09-12', '16:54:26', '16:54:26'),
	('admin', '2023-09-12', '17:01:57', '17:01:57'),
	('admin', '2023-09-12', '17:19:53', '17:19:53'),
	('admin', '2023-09-16', '01:12:01', '01:12:01'),
	('admin', '2023-09-16', '01:14:00', '01:14:00'),
	('admin', '2023-09-16', '01:14:44', '01:14:44'),
	('admin', '2023-09-16', '01:15:23', '01:15:23'),
	('admin', '2023-09-16', '01:16:09', '01:16:09'),
	('admin', '2023-09-16', '01:16:35', '01:16:35');

-- Dumping structure for procedure ssi_copy_1.newUser
DELIMITER //
CREATE PROCEDURE `newUser`()
BEGIN
    DECLARE newid INT;

    SET newid = 10;
    SELECT newid;
END//
DELIMITER ;

-- Dumping structure for table ssi_copy_1.partially_recieving_item
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

-- Dumping data for table ssi_copy_1.partially_recieving_item: ~15 rows (approximately)
INSERT INTO `partially_recieving_item` (`id`, `NAME`, `stock`, `supp_name`, `exp_date`, `reciever`, `date_recieved`) VALUES
	('R43417', 'Nutri-Vet Bladder Control Supplement for Dogs', 15, 'Pfizer corp..', NULL, 'kylde', '2023-08-23 00:00:00'),
	('R43417', 'Nutri-Vet Bladder Control Supplement for Dogs', 1, 'Pfizer corp..', NULL, 'kylde', '2023-08-23 00:00:00'),
	('R43417', 'Nutri-Vet Bladder Control Supplement for Dogs', 3, 'Pfizer corp..', NULL, 'kylde', '2023-08-28 00:00:00'),
	('R43417', 'Nutri-Vet Bladder Control Supplement for Dogs', 5, 'Pfizer corp..', NULL, 'kylde', '2023-08-28 00:00:00'),
	('Rb074c', 'Nutri-Vet Bladder Control Supplement for Dogs', 1, 'Pfizer corp..', NULL, 'kylde', '2023-08-30 00:00:00'),
	('Rb074c', 'Nutri-Vet Bladder Control Supplement for Dogs', 1, 'Pfizer corp..', NULL, 'kylde', '2023-08-30 00:00:00'),
	('Rb074c', 'Nutri-Vet Bladder Control Supplement for Dogs', 2, 'Pfizer corp..', NULL, 'kylde', '2023-08-30 00:00:00'),
	('Rb074c', 'Nutri-Vet Bladder Control Supplement for Dogs', 2, 'Pfizer corp..', NULL, 'kylde', '2023-08-30 00:00:00'),
	('R917e0', 'Fresh Step LeightWeight Clumping Cat Litter', 3, 'medVet assc..', NULL, 'kylde', '2023-08-30 00:00:00'),
	('R917e0', 'Fresh Step LeightWeight Clumping Cat Litter', 1, 'medVet assc..', NULL, 'kylde', '2023-08-30 00:00:00'),
	('R1e3d5', 'Test', 5, 'qeqw', NULL, 'admin', '2023-09-11 00:00:00'),
	('R21e64', 'UniLeash', 10, 'Robina Corp', NULL, 'admin', '2023-09-13 00:00:00'),
	('R9d3a7', 'UniLeash', 80, 'Robina Corp', NULL, 'admin', '2023-09-13 00:00:00'),
	('Ra1c30', 'Kawaki wo ameku', 50, '123', NULL, 'admin', '2023-09-14 00:00:00'),
	('Ra1c30', 'Pending', 5, '123', NULL, 'admin', '2023-09-14 00:00:00'),
	('R513E9', 'Waiting', 40, 'ABC Corporation', NULL, 'admin', '2023-09-16 00:00:00'),
	('R6B64B', 'Waiting', 5, 'Jesser Supplier Company', NULL, 'aila', '2023-09-20 00:00:00'),
	('RFFE1B', 'Waiting', 5, 'Jesser Supplier Company', NULL, 'admin', '2023-09-22 00:00:00');

-- Dumping structure for table ssi_copy_1.pet_breed
CREATE TABLE IF NOT EXISTS `pet_breed` (
  `type` varchar(32) NOT NULL,
  `breed` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table ssi_copy_1.pet_breed: ~4 rows (approximately)
INSERT INTO `pet_breed` (`type`, `breed`) VALUES
	('Dog', 'Aspin'),
	('Cat', 'Puspin'),
	('test1', 'test'),
	('Cat', 'Siamese');

-- Dumping structure for table ssi_copy_1.pet_info
CREATE TABLE IF NOT EXISTS `pet_info` (
  `id` varchar(6) NOT NULL,
  `p_name` varchar(128) NOT NULL,
  `owner_id` int(6) unsigned NOT NULL DEFAULT 0,
  `breed` varchar(32) NOT NULL,
  `type` varchar(32) NOT NULL,
  `sex` varchar(12) NOT NULL,
  `weight` varchar(12) NOT NULL,
  `bday` date NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `owner_id` (`owner_id`),
  CONSTRAINT `owner_id_FK` FOREIGN KEY (`owner_id`) REFERENCES `pet_owner_info` (`owner_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi_copy_1.pet_info: ~22 rows (approximately)
INSERT INTO `pet_info` (`id`, `p_name`, `owner_id`, `breed`, `type`, `sex`, `weight`, `bday`) VALUES
	('001431', 'Muning', 1, 'Puspin', 'Cat', 'Male', '2.5', '2023-08-16'),
	('012633', 'Bantay', 6, 'Female', 'Dog', 'Male', '50.2', '2023-08-25'),
	('015659', 'Test', 5, 'Test', 'Test', 'Test', 'Test', '2023-09-08'),
	('143436', 'Gabi', 2, 'Puspin', 'Cat', 'Male', '3', '2023-08-23'),
	('234729', 'Miru', 5, 'Puspin', 'Cat', 'Female', '1.2', '2022-12-09'),
	('234905', 'TJ', 1, 'Male', 'Dog', 'Ewan', '1', '2023-09-01'),
	('P1ec18', 'Brutus', 5, 'Mini Pin', '', 'Male', '', '2023-07-07'),
	('P40641', 'jam', 5, 'siames', 'Cat', 'Male', '1', '2023-09-12'),
	('P482dc', 'Whitey', 3, 'Bulldog', '', 'Female', '', '2023-06-23'),
	('P536ec', 'Clarence', 2, 'Human', '', 'Male', '', '2023-07-06'),
	('P62fd9', 'Clarence', 1, 'Puspin', 'Cat', 'Male', '10.5', '2023-09-20'),
	('P68ee4', 'Blacky', 3, 'Siamese', 'Cat', 'Male', '5', '2023-09-14'),
	('P6b73f', 'Browny', 3, 'Dalmatian', '', 'Male', '', '2000-12-30'),
	('P7a038', 'Riku', 29, 'Male', 'Cat', 'Puspin', '1', '2023-09-01'),
	('P7b350', 'Roko', 1, 'Puspin', 'Cat', 'Male', '10', '2023-09-15'),
	('Pb6c0b', 'Luna', 4, 'Siamese Cat', 'Cat', 'Male', '1.0', '2023-08-24'),
	('Pbf4d2', 'Bugsy', 30, 'Siamese ', 'Cat', 'Male', '5', '2022-11-22'),
	('Pc1935', 'Sol', 4, 'Calico Cat', '', 'Female', '', '2023-06-01'),
	('Pe3b3d', 'John', 3, 'Siamese', 'Cat', 'Male', '1', '2023-09-12'),
	('Pfcad9', 'Lina', 2, 'Short Hair', 'Cat', 'Female', '1.5', '2023-09-07');

-- Dumping structure for table ssi_copy_1.pet_owner_info
CREATE TABLE IF NOT EXISTS `pet_owner_info` (
  `owner_id` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `owner_name` varchar(128) NOT NULL,
  `address` varchar(256) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  PRIMARY KEY (`owner_id`),
  UNIQUE KEY `name` (`owner_name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table ssi_copy_1.pet_owner_info: ~11 rows (approximately)
INSERT INTO `pet_owner_info` (`owner_id`, `owner_name`, `address`, `contact_number`) VALUES
	(1, 'Patrick Feniza', 'Diliman, Quezon City', '09874561234'),
	(2, 'Davin Ferrancullo', 'Almar, Caloocan City', '09478056123'),
	(3, 'Joze Rizal', 'Calamba, Laguna Province', '09574794234'),
	(4, 'Christopher Landas', 'Rodriguez. Rizal ', '09076208927'),
	(5, 'James Viñas', 'Tala, Caloocan City', '09208902063'),
	(6, 'Budjette Tan', 'Trese, Manila City', '09123456789'),
	(26, 'TEST12', 'TEST12', 'TEST12'),
	(27, 'test2321', 'test2321', 'test2321'),
	(28, 'James Rubiales', 'Tet1', 'Tset'),
	(29, 'Clarence Ugay', 'Almar, Caloocan City', '0923902397'),
	(30, 'Tyrone Tuazon', 'STI College Fairview', '09831809378');

-- Dumping structure for table ssi_copy_1.recieving_item
CREATE TABLE IF NOT EXISTS `recieving_item` (
  `id` varchar(50) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
  `NAME` varchar(64) NOT NULL,
  `item_uid` varchar(6) NOT NULL,
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

-- Dumping data for table ssi_copy_1.recieving_item: ~38 rows (approximately)
INSERT INTO `recieving_item` (`id`, `NAME`, `item_uid`, `initial_stock`, `current_stock`, `supp_id`, `exp_date`, `reciever`, `state`, `date_set`, `date_recieved`) VALUES
	('1', 'Nutri-Vet Bladder Control Supplement for Dogs', 'I00005', 15, 0, 'SU000001', '2023-10-26', 'klyde', 2, '0000-00-00 00:00:00', '2023-06-12 01:49:18'),
	('2', 'Nutri-Vet Bladder Control Supplement for Dogs', 'I00005', 25, 25, 'SU000001', '2023-08-03', 'klyde', 2, '0000-00-00 00:00:00', '2023-06-12 01:57:52'),
	('R06952', 'MayPaw Heavy Duty Rope Dog Leash', 'I00001', 60, 60, 'SU000001', NULL, 'klyde', 2, '0000-00-00 00:00:00', '2023-06-14 11:39:30'),
	('R07365', 'Nutri-Vet Bladder Control Supplement for Dogs', 'I00005', 15, 15, 'SU000003', '2023-08-31', 'klyde', 2, '0000-00-00 00:00:00', '2023-06-12 02:06:53'),
	('R13022', 'Fresh Step Clumping Cat Litter', 'I00003', 4, 4, 'SU000001', NULL, 'acc_name', 2, '2023-08-30 23:42:34', '2023-08-30 23:42:43'),
	('R16f93', 'Nutri-Vet Bladder Control Supplement for Dogs', 'I00005', 21, 21, 'SU000001', NULL, 'klyde', 2, '0000-00-00 00:00:00', '2023-06-14 11:42:10'),
	('R1e3d5', 'Test', 'I10fdf', 10, 5, 'SU000001', NULL, 'acc_name', 2, '2023-09-11 23:50:09', '2023-09-16 20:36:15'),
	('R205d2', 'Taglory Rope Dog Leash', 'I00002', 50, 50, 'SU000001', NULL, 'klyde', 2, '0000-00-00 00:00:00', '2023-06-14 09:41:57'),
	('R21e64', 'UniLeash', 'I00006', 50, 40, 'SU000001', NULL, 'acc_name', 2, '2023-09-13 07:51:08', '2023-09-16 23:22:46'),
	('R275ab', 'UniLeash', 'I00006', 15, 15, 'SU000001', NULL, 'klyde', 2, '0000-00-00 00:00:00', '2023-06-14 09:50:12'),
	('R2ae83', 'MayPaw Heavy Duty Rope Dog Leash', 'I00001', 5, 5, 'SU000001', NULL, NULL, -1, '2023-08-30 23:07:19', NULL),
	('R2b87d', 'Fresh Step LeightWeight Clumping Cat Litter', 'I00004', 50, 50, 'SU000001', NULL, 'klyde', 2, '0000-00-00 00:00:00', '2023-06-14 09:51:31'),
	('R2e4c7', 'Taglory Rope Dog Leash', 'I00002', 10, 10, 'SU000001', NULL, 'acc_name', 2, '2023-08-30 23:54:15', '2023-08-30 23:54:20'),
	('R31a74', 'Fresh Step Clumping Cat Litter', 'I00003', 5, 5, 'SU000001', NULL, NULL, -1, '2023-08-30 23:05:43', NULL),
	('R40675', 'Fresh Step LeightWeight Clumping Cat Litter', 'I00004', 50, 50, 'SU000001', NULL, 'klyde', 2, '0000-00-00 00:00:00', '2023-06-14 09:50:16'),
	('R43417', 'Nutri-Vet Bladder Control Supplement for Dogs', 'I00005', 50, 41, 'SU000001', NULL, 'acc_name', 2, '2023-08-23 15:36:20', '2023-08-30 14:57:18'),
	('R513E9', 'Test ITem 003', 'I0AE71', 50, 10, 'SU000001', NULL, 'admin', 3, '2023-09-16 15:22:47', '2023-09-16 15:34:28'),
	('R59c25', 'Fresh Step LeightWeight Clumping Cat Litter', 'I00004', 15, 15, 'SU000001', NULL, 'klyde', 2, '0000-00-00 00:00:00', '2023-06-12 03:08:22'),
	('R61f49', 'MayPaw Heavy Duty Rope Dog Leash', 'I00001', 50, 50, 'SU000001', '2023-08-31', 'klyde', 2, '0000-00-00 00:00:00', '2023-06-13 20:28:05'),
	('R6838c', 'MayPaw Heavy Duty Rope Dog Leash', 'I00001', 5, 5, 'SU000001', '2023-08-29', 'acc_name', 2, '2023-08-28 12:56:18', '2023-08-28 12:56:39'),
	('R6B64B', 'Fresh Step LeightWeight Clumping Cat Litter', 'I00004', 10, 5, 'SU000004', NULL, 'aila', 3, '2023-09-16 15:28:09', '2023-09-20 09:50:44'),
	('R723f5', 'MayPaw Heavy Duty Rope Dog Leash', 'I00001', 20, 20, 'SU000001', NULL, 'acc_name', 2, '0000-00-00 00:00:00', '2023-08-23 06:56:32'),
	('R73829', 'MayPaw Heavy Duty Rope Dog Leash', 'I00001', 10, 10, 'SU000004', NULL, 'acc_name', 2, '2023-09-16 15:27:04', '2023-09-16 15:34:42'),
	('R808a6', 'UniLeash', 'I00006', 50, 50, 'SU000001', NULL, 'klyde', 2, '0000-00-00 00:00:00', '2023-06-13 17:43:22'),
	('R822b5', 'UniLeash', 'I00006', 50, 50, 'SU000001', '2023-07-27', 'klyde', 2, '0000-00-00 00:00:00', '2023-06-13 17:45:42'),
	('R86f29', 'MayPaw Heavy Duty Rope Dog Leash', 'I00001', 15, 15, 'SU000001', NULL, NULL, -1, '2023-08-30 21:54:04', NULL),
	('R917e0', 'Fresh Step LeightWeight Clumping Cat Litter', 'I00004', 5, 1, 'SU000001', NULL, 'acc_name', 2, '2023-08-30 23:53:06', '2023-08-30 23:53:59'),
	('R9d3a7', 'UniLeash', 'I00006', 90, 10, 'SU000001', NULL, 'admin', 3, '2023-09-13 09:58:01', '2023-09-13 09:58:10'),
	('Ra1c30', 'Kawaki wo ameku', 'Ia71e7', 60, 5, 'SU000001', NULL, 'admin', 3, '2023-09-14 12:04:26', '2023-09-14 12:23:13'),
	('Ra9de5', 'Taglory Rope Dog Leash', 'I00002', 50, 50, 'SU000001', NULL, NULL, -1, '2023-08-30 20:33:34', NULL),
	('Rae388', 'MayPaw Heavy Duty Rope Dog Leash', 'I00001', 10, 10, 'SU000001', NULL, 'acc_name', 2, '2023-08-30 23:43:11', '2023-08-30 23:43:28'),
	('Rb074c', 'Nutri-Vet Bladder Control Supplement for Dogs', 'I00005', 10, 4, 'SU000001', '2023-09-28', 'acc_name', 2, '2023-08-30 23:43:49', '2023-08-30 23:52:33'),
	('Rb556f', 'Taglory Rope Dog Leash', 'I00002', 5, 5, 'SU000001', NULL, 'acc_name', 2, '2023-08-23 06:54:02', '2023-08-26 14:38:02'),
	('Rc0b6a', 'Taglory Rope Dog Leash', 'I00002', 50, 50, 'SU000001', NULL, 'acc_name', 2, '0000-00-00 00:00:00', '2023-08-23 06:40:06'),
	('Rd584c', 'MayPaw Heavy Duty Rope Dog Leash', 'I00001', 55, 55, 'SU000001', NULL, 'acc_name', 2, '2023-08-30 14:58:50', '2023-08-30 14:58:56'),
	('Rdf3a5', 'Test Item', 'Iaad08', 10, 10, 'SU000001', NULL, 'acc_name', 2, '2023-09-14 12:09:10', '2023-09-16 20:35:59'),
	('RFFE1B', 'Test', 'I10fdf', 10, 5, 'SU000004', NULL, 'admin', 3, '2023-09-16 15:25:28', '2023-09-22 11:26:51'),
	('Rf166d', 'MayPaw Heavy Duty Rope Dog Leash', 'I00001', 15, 15, 'SU000001', NULL, 'klyde', 2, '0000-00-00 00:00:00', '2023-06-12 03:08:47');

-- Dumping structure for table ssi_copy_1.services_transaction_content
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
  KEY `transaction_uid` (`transaction_uid`),
  KEY `FK_services_transaction_content_pet_info` (`pet_uid`),
  CONSTRAINT `FK_services_transaction_content_pet_info` FOREIGN KEY (`pet_uid`) REFERENCES `pet_info` (`id`),
  CONSTRAINT `FK_services_transaction_content_transaction_record` FOREIGN KEY (`transaction_uid`) REFERENCES `transaction_record` (`transaction_uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi_copy_1.services_transaction_content: ~0 rows (approximately)

-- Dumping structure for table ssi_copy_1.service_category_test
CREATE TABLE IF NOT EXISTS `service_category_test` (
  `category` varchar(64) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `state` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table ssi_copy_1.service_category_test: ~5 rows (approximately)
INSERT INTO `service_category_test` (`category`, `state`) VALUES
	('Grooming', 1),
	('Pet Care', 1),
	('Surgery', 1),
	('Test', 1),
	('Vaccination', 1);

-- Dumping structure for table ssi_copy_1.service_info
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

-- Dumping data for table ssi_copy_1.service_info: ~8 rows (approximately)
INSERT INTO `service_info` (`UID`, `service_name`, `Item_needed`, `price`, `state`, `date_added`) VALUES
	('S00001', 'Grooming', 'test', 500, 1, '2023-05-29'),
	('S00002', '5-in-1 Vaccine', 'test', 1500, 1, '2023-05-29'),
	('S00003', 'Papiloma Vaccine', 'test', 2500, 1, '2023-05-29'),
	('S00004', 'Yeast Infection Treatment', 'test', 2100, 1, '2023-05-29'),
	('S00005', 'Canine Castration Surgery', 'test', 1700, 1, '2023-05-29'),
	('S00006', 'Confinement', 'test', 200, 1, '2023-05-29'),
	('S00007', 'Euthanasion', 'test', 900, 1, '2023-05-29'),
	('S00008', 'Feline Castration Srugery', 'test', 500, 1, '2023-05-29');

-- Dumping structure for table ssi_copy_1.service_info_test
CREATE TABLE IF NOT EXISTS `service_info_test` (
  `UID` varchar(6) NOT NULL,
  `service_name` varchar(256) NOT NULL,
  `price` float NOT NULL,
  `category` varchar(64) NOT NULL,
  `duration_type` int(1) NOT NULL,
  `state` int(1) NOT NULL,
  `date_added` date NOT NULL,
  PRIMARY KEY (`UID`) USING BTREE,
  UNIQUE KEY `service_name` (`service_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci ROW_FORMAT=DYNAMIC;

-- Dumping data for table ssi_copy_1.service_info_test: ~8 rows (approximately)
INSERT INTO `service_info_test` (`UID`, `service_name`, `price`, `category`, `duration_type`, `state`, `date_added`) VALUES
	('S00001', 'Grooming', 500, 'Grooming', 0, 1, '2023-05-29'),
	('S00002', '5-in-1 Vaccine', 1500, 'Vaccination', 0, 1, '2023-05-29'),
	('S00003', 'Papiloma Vaccine', 2500, 'Vaccination', 0, 1, '2023-05-29'),
	('S00004', 'Yeast Infection Treatment', 2100, 'Pet Care', 0, 1, '2023-05-29'),
	('S00005', 'Canine Castration Surgery', 1700, 'Surgery', 0, 1, '2023-05-29'),
	('S00006', 'Confinement', 200, 'Pet Care', 1, 1, '2023-05-29'),
	('S00008', 'Feline Castration Srugery', 500, 'Surgery', 0, 1, '2023-05-29'),
	('Se7c43', 'Canine Diagnostic', 1200, 'Pet Care', 0, 1, '2023-08-31');

-- Dumping structure for table ssi_copy_1.supplier_info
CREATE TABLE IF NOT EXISTS `supplier_info` (
  `supp_id` varchar(8) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `supp_name` varchar(128) NOT NULL,
  `contact_person` varchar(128) NOT NULL,
  `contact_number` varchar(32) NOT NULL,
  `contact_email` varchar(128) DEFAULT NULL,
  `address` varchar(256) NOT NULL,
  `created_by` varchar(128) NOT NULL,
  `date_added` datetime NOT NULL,
  `date_modified` datetime DEFAULT NULL,
  PRIMARY KEY (`supp_id`),
  UNIQUE KEY `supp_name` (`supp_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table ssi_copy_1.supplier_info: ~7 rows (approximately)
INSERT INTO `supplier_info` (`supp_id`, `supp_name`, `contact_person`, `contact_number`, `contact_email`, `address`, `created_by`, `date_added`, `date_modified`) VALUES
	('SU000001', 'ABC Corporation', 'James Vinas', '09457891234', NULL, 'Quezon City', 'admin', '2023-09-15 00:00:00', NULL),
	('SU000002', 'XYZ Corporation', 'Ryan Gosling', '01234567890', 'ryangosling@gmail.com', 'Quezon City', 'admin', '2023-09-15 20:40:22', NULL),
	('SU000003', 'UP Veterinary Supplies', 'Jesus Rizal', '0914 486 2143', 'upveterinary@gmail.com', 'UP Diliman, Quezon City', 'admin', '2023-09-15 21:41:26', '2023-09-16 02:39:51'),
	('SU000004', 'Jesser Supplier Company', 'Jesser Famorca', '0154 467 3571', 'jesser.famorca@testcompany.com', 'Quezon City', 'admin', '2023-09-15 23:20:06', '2023-09-16 09:48:53'),
	('SU000005', 'Med Corporation', 'Dan Brown', '09875641243', 'danbrown@medcorp.net', 'Manila City', 'admin', '2023-09-16 00:11:33', NULL),
	('SU000006', 'BreadCrumb Corp.', 'James Rubiales', '09745734891', 'NULL', 'Manila, Manila City', 'admin', '2023-09-16 14:11:36', NULL),
	('SU000007', 'JKL Corp', 'Jose Rizal', '09208902063', 'jkl@gmail.com', 'QC', 'aila', '2023-09-20 09:45:47', NULL);

-- Dumping structure for table ssi_copy_1.transaction_record
CREATE TABLE IF NOT EXISTS `transaction_record` (
  `transaction_uid` varchar(8) NOT NULL,
  `Attendant_usn` varchar(128) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
  `client_name` varchar(50) DEFAULT NULL,
  `Total_amount` float NOT NULL,
  `transaction_date` date NOT NULL,
  PRIMARY KEY (`transaction_uid`),
  KEY `Attendant_usn` (`Attendant_usn`),
  CONSTRAINT `transaction_record_ibfk_1` FOREIGN KEY (`Attendant_usn`) REFERENCES `acc_cred` (`usn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Dumping data for table ssi_copy_1.transaction_record: ~78 rows (approximately)
INSERT INTO `transaction_record` (`transaction_uid`, `Attendant_usn`, `client_name`, `Total_amount`, `transaction_date`) VALUES
	('0', 'aila', 'N/A', 1045, '2023-07-14'),
	('1', 'aila', 'James V.', 500, '2023-07-15'),
	('10', 'aila', 'Jose R.', 500, '2023-08-01'),
	('11', 'aila', 'N/A', 440, '2023-08-06'),
	('12', 'aila', 'James V.', 900, '2023-08-06'),
	('13', 'aila', 'James V.', 500, '2023-08-07'),
	('14', 'aila', 'N/A', 1320, '2023-08-07'),
	('15', 'aila', 'N/A', 880, '2023-08-14'),
	('16', 'aila', 'N/A', 2033.9, '2023-08-14'),
	('17', 'aila', 'James V.', 1380, '2023-08-20'),
	('18', 'aila', 'James V.', 500, '2023-08-20'),
	('19', 'aila', 'N/A', 880, '2023-08-20'),
	('2', 'aila', 'N/A', 440, '2023-07-15'),
	('20', 'aila', 'James V.', 1500, '2023-08-20'),
	('21', 'aila', 'James V.', 500, '2023-08-22'),
	('22', 'aila', 'Davin F.', 500, '2023-08-22'),
	('23', 'aila', 'N/A', 440, '2023-08-22'),
	('24', 'aila', 'N/A', 2200, '2023-08-22'),
	('25', 'aila', 'N/A', 440, '2023-08-22'),
	('26', 'aila', 'N/A', 440, '2023-08-22'),
	('27', 'aila', 'N/A', 440, '2023-08-22'),
	('28', 'aila', 'N/A', 1320, '2023-08-22'),
	('29', 'aila', 'N/A', 440, '2023-08-22'),
	('3', 'aila', 'N/A', 3420.45, '2023-07-16'),
	('30', 'aila', 'N/A', 1320, '2023-08-22'),
	('31', 'aila', 'N/A', 440, '2023-08-22'),
	('32', 'aila', 'N/A', 1760, '2023-08-23'),
	('33', 'aila', 'Jose R.', 440, '2023-08-23'),
	('34', 'aila', 'N/A', 796.95, '2023-08-23'),
	('35', 'aila', 'James V.', 2280.3, '2023-08-26'),
	('36', 'aila', 'N/A', 2310, '2023-08-28'),
	('37', 'aila', 'N/A', 2171.4, '2023-08-28'),
	('38', 'aila', 'Jose R.', 0, '2023-08-28'),
	('39', 'aila', 'N/A', 577.5, '2023-08-29'),
	('4', 'aila', 'James V.', 500, '2023-07-16'),
	('41', 'aila', 'Bud Tan', 1500, '2023-08-29'),
	('42', 'aila', 'James V.', 500, '2023-08-29'),
	('43', 'aila', 'Bud Tan', 500, '2023-08-29'),
	('44', 'aila', 'Bud Tan', 500, '2023-08-30'),
	('45', 'aila', 'James V.', 500, '2023-08-30'),
	('46', 'aila', 'N/A', 577.5, '2023-08-30'),
	('47', 'aila', 'N/A', 577.5, '2023-08-30'),
	('48', 'aila', 'Christopher L.', 2310, '2023-08-30'),
	('49', 'admin', 'N/A', 522.5, '2023-08-30'),
	('5', 'aila', 'Jose R.', 1000, '2023-07-16'),
	('50', 'admin', 'James V.', 1567.5, '2023-08-30'),
	('51', 'admin', 'N/A', 577.5, '2023-08-30'),
	('52', 'admin', 'Bud Tan', 1567.5, '2023-08-31'),
	('53', 'admin', 'N/A', 1045, '2023-08-31'),
	('54', 'admin', 'N/A', 1155, '2023-08-31'),
	('55', 'admin', 'N/A', 522.5, '2023-08-31'),
	('56', 'admin', 'N/A', 522.5, '2023-08-31'),
	('57', 'admin', 'N/A', 522.5, '2023-08-31'),
	('58', 'admin', 'N/A', 1567.5, '2023-08-31'),
	('59', 'admin', 'N/A', 522.5, '2023-09-02'),
	('6', 'aila', 'N/A', 3187.8, '2023-07-13'),
	('60', 'admin', 'James V.', 2780.3, '2023-09-02'),
	('61', 'admin', 'Bud Tan', 500, '2023-09-02'),
	('62', 'admin', 'Patrick Feniza', 500, '2023-09-02'),
	('63', 'admin', 'James V.', 1000, '2023-09-03'),
	('64', 'admin', 'Davin F.', 2500, '2023-09-03'),
	('65', 'admin', 'Jose R.', 1000, '2023-09-03'),
	('66', 'admin', 'James V.', 500, '2023-09-03'),
	('67', 'admin', 'Patrick Feniza', 500, '2023-09-03'),
	('68', 'admin', 'Bud Tan', 500, '2023-09-03'),
	('69', 'admin', 'Patrick Feniza', 500, '2023-09-03'),
	('7', 'aila', 'Jose R.', 1000, '2023-07-13'),
	('70', 'admin', 'James V.', 3000, '2023-09-03'),
	('71', 'admin', 'Patrick Feniza', 2500, '2023-09-03'),
	('72', 'admin', 'Davin F.', 4600, '2023-09-03'),
	('73', 'admin', 'James V.', 2100, '2023-09-03'),
	('74', 'admin', 'Patrick Feniza', 2000, '2023-09-03'),
	('75', 'admin', 'N/A', 2280.3, '2023-09-03'),
	('76', 'admin', 'N/A', 2280.3, '2023-09-03'),
	('77', 'admin', 'N/A', 288, '2023-09-03'),
	('78', 'Jrizal', 'Christopher L.', 2500, '2023-09-03'),
	('79', 'admin', 'James Viñas', 4500, '2023-09-07'),
	('8', 'aila', 'N/A', 1593.9, '2023-08-01'),
	('9', 'aila', 'N/A', 144, '2023-08-01');

-- Dumping structure for table ssi_copy_1.user_level_access
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

-- Dumping data for table ssi_copy_1.user_level_access: ~2 rows (approximately)
INSERT INTO `user_level_access` (`Title`, `add_item`, `Dashboard`, `Reception`, `Payment`, `Services`, `Sales`, `Inventory`, `Pet_Info`, `Report`, `User`, `Action`, `Gen_Settings`) VALUES
	('Assisstant', 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0),
	('Owner', 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
