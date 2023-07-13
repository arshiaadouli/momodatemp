-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 19, 2023 at 12:54 AM
-- Server version: 10.6.12-MariaDB-cll-lve
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `u528062626_momoda`
--

-- --------------------------------------------------------

--
-- Table structure for table `users_user`
--

CREATE TABLE `users_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `email` varchar(60) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `first_name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `last_name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `orcid` varchar(19) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `date_created` datetime NOT NULL,
  `is_private` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `is_active` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `is_staff` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `is_superuser` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users_user`
--

INSERT INTO `users_user` (`id`, `password`, `last_login`, `email`, `first_name`, `last_name`, `orcid`, `date_created`, `is_private`, `is_active`, `is_staff`, `is_superuser`) VALUES
(2, 'pbkdf2_sha256$390000$vtj6fTp22IZfOeCxbDP8kK$ToBhyj+9Q2Nyy20wkv0HjZutNN192M31FuLpfgXrk1s=', NULL, 'arshiaadouli@gmail.com', 'Arshia', 'Adouli', '', '2022-08-26 11:18:21', '1', '1', '0', '0'),
(3, 'pbkdf2_sha256$600000$NQtgNYV3HNpwuBWybPwfzg$uDtmKyePGFXll/zxrINGv+BSs/Dnu8KjQ7AwkFzN05Q=', '2023-05-13 16:40:52', 'aado0001@student.monash.edu', 'arshia', 'adouli', '', '2022-08-26 11:19:43', '1', '1', '0', '0'),
(6, 'pbkdf2_sha256$390000$pllvfL7n5yC2T6H8IirK6r$ie2mhCFycXUsLjgANHtxqfFBHr3dWMMTAsfgnFHNtCY=', '2023-05-07 22:52:52', 'mnem0001@student.monash.edu', 'Milad', 'Nemati', '', '2022-08-23 06:28:53', '1', '1', '1', '1');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users_user`
--
ALTER TABLE `users_user`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD UNIQUE KEY `sqlite_autoindex_users_user_1` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users_user`
--
ALTER TABLE `users_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
