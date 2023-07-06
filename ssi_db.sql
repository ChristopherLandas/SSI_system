/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

INSERT INTO `account_access_level` (`usn`, `Dashboard`, `Transaction`, `Services`, `Sales`, `Inventory`, `Pet_Info`, `Report`, `User`, `Action`) VALUES
	('admin', 1, 1, 1, 1, 1, 1, 1, 1, 1),
	('aila', 0, 0, 1, 1, 1, 1, 1, 0, 0),
	('assisstant', 1, 1, 1, 1, 1, 1, 1, 0, 0),
	('Chris', 1, 1, 1, 1, 0, 0, 1, 0, 0),
	('Jrizal', 1, 1, 1, 1, 1, 1, 1, 0, 0),
	('jayr', 0, 1, 0, 0, 0, 0, 0, 0, 0);

INSERT INTO `acc_cred` (`usn`, `pss`, `slt`, `entry_OTP`) VALUES
	('admin', '0c149295209d5f543cf1ba14956c5c135a78b9b311ad551715899e02c27dc99d', 'rCRF4amTSEOYQjqvWYuI7A==', NULL),
	('aila', 'b94fd2a2585dada0d309427f886092192a58ce549056edd56df595623b01cef9', 'ND08SurlSBKB74ch5HD9iQ==', NULL),
	('assisstant', '5362ca593f063f2581f756e9827bdd02da670bad2b176108380d7bc971ee5148', 'ljEGlbKwSZe3ECK-0b2K8g==', NULL),
	('Chris', '85f66b5cb989b9d7910c5b4ee119023ef079097541911ca459e0d0622084403e', 'WSmvZucFRmyDhLpovauFAQ==', NULL),
	('Jrizal', '4436a253401b8e74a80e7a9a04930e16ae6e37dbc8c36f49f871ead477044f53', '3wbtXJDmSTm98iubl13hLw==', NULL),
	('jayr', '56a1f73718b12d1a021f12eee52d2d1bbe1e6c067698c27e98c5fdd22fb0a0dd', 'WqMM26lyQDirax7evZgFuQ==', NULL);

INSERT INTO `acc_info` (`usn`, `full_name`, `job_position`) VALUES
	('admin', 'Owner', 'Owner'),
	('aila', 'aila', 'Assisstant'),
	('assisstant', 'Assisstant', 'Assisstant'),
	('Chris', 'Chris McLaind', 'Assisstant'),
	('Jrizal', 'Jose Rizal', 'Assisstant'),
	('jayr', 'jayr', 'Assisstant');


INSERT INTO `categories` (`categ_name`, `does_expire`) VALUES
	('Accessories', 0),
	('Food', 1),
	('Medicine', 1),
	('test', 0);

INSERT INTO `disposal_history` (`id`, `item_name`, `quan`, `date_of_disposal`, `disposed_by`) VALUES
	(1, 'MayPaw Heavy Duty Rope Dog Leash', 12, '2023-06-11 03:22:39', 'klyde'),
	(2, 'Nutri-Vet Bladder Control Supplement for Dogs', 48, '2023-06-13 17:30:25', 'klyde'),
	(3, 'Nutri-Vet Bladder Control Supplement for Dogs', 5, '2023-06-14 09:15:53', 'klyde');

INSERT INTO `item_general_info` (`UID`, `name`, `Category`) VALUES
	('I00001', 'MayPaw Heavy Duty Rope Dog Leash', 'Accessories'),
	('I00002', 'Taglory Rope Dog Leash', 'Accessories'),
	('I00003', 'Fresh Step Clumping Cat Litter', 'Accessories'),
	('I00004', 'Fresh Step LeightWeight Clumping Cat Litter', 'Accessories'),
	('I00005', 'Nutri-Vet Bladder Control Supplement for Dogs', 'Medicine'),
	('I00006', 'UniLeash', 'Accessories');

INSERT INTO `item_inventory_info` (`UID`, `Stock`, `Expiry_Date`) VALUES
	('I00001', 908, NULL),
	('I00002', 54, NULL),
	('I00003', 66, NULL),
	('I00004', 55, NULL),
	('I00005', 114, '2023-10-26'),
	('I00005', 45, '2023-08-31'),
	('I00006', 80, NULL),
	('I00005', 21, NULL);

INSERT INTO `item_settings` (`UID`, `Cost_Price`, `Markup_Factor`, `Reorder_factor`, `Crit_factor`, `Safe_stock`) VALUES
	('I00001', 475, 0.1, 0.85, 0.5, 50),
	('I00002', 400, 0.1, 0.85, 0.5, 50),
	('I00003', 525, 0.1, 0.85, 0.5, 25),
	('I00004', 724.5, 0.1, 0.85, 0.5, 25),
	('I00005', 1036.5, 0.1, 0.85, 0.5, 85),
	('I00006', 120, 0.2, 0.75, 0.5, 15);

INSERT INTO `item_supplier_info` (`UID`, `Supplier`, `Contacts`) VALUES
	('I00001', 'ABC corp.', 'ABCcorp@gmail.com'),
	('I00002', 'ABC corp.', 'ABCcorp@gmail.com'),
	('I00003', 'medVet assc.', '+639042648221'),
	('I00004', 'medVet assc..', '+639042648221'),
	('I00005', 'Pfizer corp..', 'OrtSupp@Pfizer.com.ph'),
	('I00006', 'Robina Corp', '');

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
	('37', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('38', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('38', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('38', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('38', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('38', 'I00002', 'Taglory Rope Dog Leash', 1, 440, 0),
	('38', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('38', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('39', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('40', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('41', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('42', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('44', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('45', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('46', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('47', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 1, 522.5, 0),
	('48', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 12, 522.5, 0),
	('49', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 15, 522.5, 0),
	('50', 'I00001', 'MayPaw Heavy Duty Rope Dog Leash', 3, 522.5, 0),
	('54', 'I00002', 'Taglory Rope Dog Leash', 45, 440, 0),
	('55', 'I00004', 'Fresh Step LeightWeight Clumping Cat Litter', 70, 796.95, 0),
	('56', 'I00004', 'Fresh Step LeightWeight Clumping Cat Litter', 50, 796.95, 0);

INSERT INTO `login_report` (`attempt_usn`, `usn_used`, `date_created`) VALUES
	(NULL, 'admin', '2023-06-07 23:50:59'),
	('admin', 'admin', '2023-06-07 23:54:09'),
	('admin', 'admin', '2023-06-07 23:55:45'),
	(NULL, 'chris', '2023-07-05 17:36:56');

INSERT INTO `log_history` (`usn`, `date_logged`, `time_in`, `time_out`) VALUES
	('admin', '2023-05-29', '22:34:57', '22:34:57'),
	('admin', '2023-05-29', '22:37:24', '22:37:24');

INSERT INTO `pet_info` (`id`, `o_name`, `p_name`, `breed`, `sex`, `bday`, `address`, `contact`) VALUES
	('P482dc', 'Jose R.', 'Whitey', 'Bulldog', 'Female', '2023-06-23', 'QC', '+639076208297'),
	('P6b73f', 'Jose R.', 'Browny', 'Dalmatian', 'Male', '2000-12-30', 'QC', '+639076208297'),
	('Pb6c0b', 'Christopher L.', 'Puchi', 'Siamese Cat', 'Male', '2023-08-24', 'Bl7 Lt322 Ph2-A GreenBreeze Subd. Rod, Rizal', '+639076208297'),
	('Pc1935', 'Christopher L.', 'Sol', 'Calico Cat', 'Female', '2023-06-01', 'Bl7 Lt322 Ph2-A GreenBreeze Subd. Rod, Rizal', '+639076208297');

INSERT INTO `recieving_item` (`id`, `NAME`, `stock`, `supp_name`, `exp_date`, `reciever`, `state`, `date_recieved`) VALUES
	('1', 'Nutri-Vet Bladder Control Supplement for Dogs', 15, 'Pfizer corp..', '2023-10-26', 'klyde', 2, '2023-06-12 01:49:18'),
	('2', 'Nutri-Vet Bladder Control Supplement for Dogs', 25, 'Pfizer corp..', '2023-08-03', 'klyde', 2, '2023-06-12 01:57:52'),
	('R06952', 'MayPaw Heavy Duty Rope Dog Leash', 60, 'ABC corp.', NULL, 'klyde', 2, '2023-06-14 11:39:30'),
	('R07365', 'Nutri-Vet Bladder Control Supplement for Dogs', 15, 'Pfizer corp..', '2023-08-31', 'klyde', 2, '2023-06-12 02:06:53'),
	('R16f93', 'Nutri-Vet Bladder Control Supplement for Dogs', 21, 'Pfizer corp..', NULL, 'klyde', 2, '2023-06-14 11:42:10'),
	('R205d2', 'Taglory Rope Dog Leash', 50, 'ABC corp.', NULL, 'klyde', 2, '2023-06-14 09:41:57'),
	('R275ab', 'UniLeash', 15, 'Robina Corp', NULL, 'klyde', 2, '2023-06-14 09:50:12'),
	('R2b87d', 'Fresh Step LeightWeight Clumping Cat Litter', 50, 'medVet assc..', NULL, 'klyde', 2, '2023-06-14 09:51:31'),
	('R40675', 'Fresh Step LeightWeight Clumping Cat Litter', 50, 'medVet assc..', NULL, 'klyde', 2, '2023-06-14 09:50:16'),
	('R59c25', 'Fresh Step LeightWeight Clumping Cat Litter', 15, 'medVet assc..', NULL, 'klyde', 2, '2023-06-12 03:08:22'),
	('R61f49', 'MayPaw Heavy Duty Rope Dog Leash', 50, 'ABC corp.', '2023-08-31', 'klyde', 2, '2023-06-13 20:28:05'),
	('R808a6', 'UniLeash', 50, 'Robina Corp.', NULL, 'klyde', 2, '2023-06-13 17:43:22'),
	('R822b5', 'UniLeash', 50, 'Robina Corp', '2023-07-27', 'klyde', 2, '2023-06-13 17:45:42'),
	('Rf166d', 'MayPaw Heavy Duty Rope Dog Leash', 15, 'ABC corp.', NULL, 'klyde', 2, '2023-06-12 03:08:47');

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
	('36', 'S00002', '5-in-1 Vaccine', 'rex', '2023-06-29', 1500, 0, 0),
	('38', 'S00001', 'Grooming', 'Puchi', '2023-06-14', 500, 0, 0),
	('38', 'S00001', 'Grooming', 'Puchi', '2023-06-14', 500, 0, 0),
	('38', 'S00001', 'Grooming', 'Sol', '2023-06-14', 500, 0, 0),
	('39', 'S00001', 'Grooming', 'Puchi', '2023-06-14', 500, 0, 0),
	('43', 'S00001', 'Grooming', 'Puchi', '2023-06-14', 500, 0, 0),
	('51', 'S00003', 'Papiloma Vaccine', 'Sol', '2023-06-14', 2500, 0, 0),
	('52', 'S00001', 'Grooming', 'Whitey', '2023-06-14', 500, 0, 0),
	('53', 'S00001', 'Grooming', 'Whitey', '2023-06-14', 500, 0, 0);

INSERT INTO `service_info` (`UID`, `service_name`, `Item_needed`, `price`, `state`, `date_added`) VALUES
	('S00001', 'Grooming', 'test', 500, 1, '2023-05-29'),
	('S00002', '5-in-1 Vaccine', 'test', 1500, 1, '2023-05-29'),
	('S00003', 'Papiloma Vaccine', 'test', 2500, 1, '2023-05-29'),
	('S00004', 'Yeast Infection Treatment', 'test', 2100, 1, '2023-05-29'),
	('S00005', 'Canine Castration Surgery', 'test', 1700, 1, '2023-05-29'),
	('S00006', 'Confinement', 'test', 200, 1, '2023-05-29'),
	('S00007', 'Euthanasion', 'test', 900, 1, '2023-05-29'),
	('S00008', 'Feline Castration Srugery', 'test', 500, 1, '2023-05-29');

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
	('37', 'admin', 'rex', 522.5, '2023-06-10'),
	('38', 'admin', 'N/A', 522.5, '2023-06-14'),
	('39', 'admin', 'N/A', 1022.5, '2023-06-14'),
	('40', 'admin', 'N/A', 522.5, '2023-06-14'),
	('41', 'admin', 'N/A', 522.5, '2023-06-14'),
	('42', 'admin', 'N/A', 522.5, '2023-06-14'),
	('43', 'admin', 'N/A', 500, '2023-06-14'),
	('44', 'admin', 'N/A', 522.5, '2023-06-14'),
	('45', 'admin', 'N/A', 522.5, '2023-06-14'),
	('46', 'admin', 'N/A', 522.5, '2023-06-14'),
	('47', 'admin', 'N/A', 522.5, '2023-06-14'),
	('48', 'admin', 'N/A', 18810, '2023-06-14'),
	('49', 'admin', 'N/A', 7837.5, '2023-06-14'),
	('50', 'admin', 'N/A', 1567.5, '2023-06-14'),
	('51', 'admin', 'N/A', 2500, '2023-06-14'),
	('52', 'admin', 'N/A', 500, '2023-06-14'),
	('53', 'admin', 'N/A', 500, '2023-06-14'),
	('54', 'admin', 'N/A', 19800, '2023-06-14'),
	('55', 'admin', 'N/A', 55786.5, '2023-06-14'),
	('56', 'admin', 'N/A', 39847.5, '2023-06-14');

INSERT INTO `user_level_access` (`Title`, `add_item`, `Dashboard`, `Transaction`, `Services`, `Sales`, `Inventory`, `Pet_Info`, `Report`, `User`, `Action`) VALUES
	('Assisstant', 0, 1, 1, 1, 1, 1, 1, 1, 0, 0),
	('Owner', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
