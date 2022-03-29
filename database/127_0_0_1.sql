-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 29, 2022 at 02:33 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 7.4.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `peminjamanbuku_db`
--
CREATE DATABASE IF NOT EXISTS `peminjamanbuku_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `peminjamanbuku_db`;

-- --------------------------------------------------------

--
-- Table structure for table `tanggota`
--

CREATE TABLE `tanggota` (
  `NIM` varchar(20) NOT NULL,
  `namaMhs` varchar(100) NOT NULL,
  `jurusan` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tanggota`
--

INSERT INTO `tanggota` (`NIM`, `namaMhs`, `jurusan`) VALUES
('3214', '3214', '43214'),
('3333', '333', '3333');

-- --------------------------------------------------------

--
-- Table structure for table `tbuku`
--

CREATE TABLE `tbuku` (
  `kodeBuku` varchar(10) NOT NULL,
  `judul` varchar(100) NOT NULL,
  `stok` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tbuku`
--

INSERT INTO `tbuku` (`kodeBuku`, `judul`, `stok`) VALUES
('2131', '1231', 10),
('tes2', 'tes2', 12);

-- --------------------------------------------------------

--
-- Table structure for table `tkembali`
--

CREATE TABLE `tkembali` (
  `kodeKembali` varchar(10) NOT NULL,
  `kodeBuku` varchar(10) NOT NULL,
  `NIM` varchar(20) NOT NULL,
  `tglKembali` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tkembali`
--

INSERT INTO `tkembali` (`kodeKembali`, `kodeBuku`, `NIM`, `tglKembali`) VALUES
('3123', 'tes2', '3214', '2022-03-18'),
('626515', '2131', '3214', '2022-03-16');

-- --------------------------------------------------------

--
-- Table structure for table `tpinjam`
--

CREATE TABLE `tpinjam` (
  `kodePinjam` varchar(10) NOT NULL,
  `kodeBuku` varchar(10) NOT NULL,
  `NIM` varchar(20) NOT NULL,
  `tglPinjam` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tpinjam`
--

INSERT INTO `tpinjam` (`kodePinjam`, `kodeBuku`, `NIM`, `tglPinjam`) VALUES
('12', 'tes2', '3214', '2022-03-17'),
('1234', '2131', '3333', '2022-03-17'),
('3336', '2131', '3214', '2022-03-10'),
('6665', '2131', '3214', '2022-03-17');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`username`, `password`) VALUES
('admin', 'admin123'),
('pergun', 'pergun451');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tanggota`
--
ALTER TABLE `tanggota`
  ADD PRIMARY KEY (`NIM`);

--
-- Indexes for table `tbuku`
--
ALTER TABLE `tbuku`
  ADD PRIMARY KEY (`kodeBuku`);

--
-- Indexes for table `tkembali`
--
ALTER TABLE `tkembali`
  ADD PRIMARY KEY (`kodeKembali`),
  ADD KEY `kodeBuku` (`kodeBuku`),
  ADD KEY `NIM` (`NIM`);

--
-- Indexes for table `tpinjam`
--
ALTER TABLE `tpinjam`
  ADD PRIMARY KEY (`kodePinjam`),
  ADD KEY `kodeBuku` (`kodeBuku`),
  ADD KEY `NIM` (`NIM`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`username`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tkembali`
--
ALTER TABLE `tkembali`
  ADD CONSTRAINT `tkembali_ibfk_1` FOREIGN KEY (`kodeBuku`) REFERENCES `tbuku` (`kodeBuku`),
  ADD CONSTRAINT `tkembali_ibfk_2` FOREIGN KEY (`NIM`) REFERENCES `tanggota` (`NIM`);

--
-- Constraints for table `tpinjam`
--
ALTER TABLE `tpinjam`
  ADD CONSTRAINT `tpinjam_ibfk_1` FOREIGN KEY (`kodeBuku`) REFERENCES `tbuku` (`kodeBuku`),
  ADD CONSTRAINT `tpinjam_ibfk_2` FOREIGN KEY (`NIM`) REFERENCES `tanggota` (`NIM`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
