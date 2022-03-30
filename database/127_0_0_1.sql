-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 29 Mar 2022 pada 17.04
-- Versi server: 10.4.18-MariaDB
-- Versi PHP: 8.0.3

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
-- Struktur dari tabel `tanggota`
--

CREATE TABLE `tanggota` (
  `NIM` varchar(20) NOT NULL,
  `namaMhs` varchar(100) NOT NULL,
  `jurusan` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `tanggota`
--

INSERT INTO `tanggota` (`NIM`, `namaMhs`, `jurusan`) VALUES
('32190034', 'Felix Setiawan', 'Teknik Informatika'),
('32190041', 'Kelvin Chandra', 'Teknik Informatika'),
('32190048', 'Kevin Kusuma', 'Teknik Informatika'),
('32190052', 'Samuel Sulianto', 'Teknik Informatika'),
('32190097', 'Reynaldo Krisno', 'Teknik Informatika'),
('32190098', 'Ferry Gunawan', 'Teknik Informatika');

-- --------------------------------------------------------

--
-- Struktur dari tabel `tbuku`
--

CREATE TABLE `tbuku` (
  `kodeBuku` varchar(10) NOT NULL,
  `judul` varchar(100) NOT NULL,
  `stok` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `tbuku`
--

INSERT INTO `tbuku` (`kodeBuku`, `judul`, `stok`) VALUES
('B01', '7 in 1 Pemrograman Web untuk Pemula', 10),
('B02', 'DEMON SLAYER Kimetsu no Yaiba 08', 4),
('B03', 'Detektif Conan 99', 7),
('B04', 'Jujutsu Kaisen 05', 3),
('B05', 'Masakan Rumahan Lezat Dan Nikmat', 13),
('B06', 'Merancang Aplikasi Dengan Metodologi Extreme Programmings', 25),
('B07', 'Panduan Praktis Budidaya Dan Pemeliharaan Cupang', 55),
('B08', 'Pemrograman Web Berbasis HTML 5, PHP, Dan JavaScript', 1);

-- --------------------------------------------------------

--
-- Struktur dari tabel `tkembali`
--

CREATE TABLE `tkembali` (
  `kodeKembali` varchar(10) NOT NULL,
  `kodeBuku` varchar(10) NOT NULL,
  `NIM` varchar(20) NOT NULL,
  `tglKembali` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tpinjam`
--

CREATE TABLE `tpinjam` (
  `kodePinjam` varchar(10) NOT NULL,
  `kodeBuku` varchar(10) NOT NULL,
  `NIM` varchar(20) NOT NULL,
  `tglPinjam` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `user`
--

CREATE TABLE `user` (
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `user`
--

INSERT INTO `user` (`username`, `password`) VALUES
('admin', 'admin123'),
('chandra', 'kelvin123'),
('pergun', 'pergun451');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `tanggota`
--
ALTER TABLE `tanggota`
  ADD PRIMARY KEY (`NIM`);

--
-- Indeks untuk tabel `tbuku`
--
ALTER TABLE `tbuku`
  ADD PRIMARY KEY (`kodeBuku`);

--
-- Indeks untuk tabel `tkembali`
--
ALTER TABLE `tkembali`
  ADD PRIMARY KEY (`kodeKembali`),
  ADD KEY `kodeBuku` (`kodeBuku`),
  ADD KEY `NIM` (`NIM`);

--
-- Indeks untuk tabel `tpinjam`
--
ALTER TABLE `tpinjam`
  ADD PRIMARY KEY (`kodePinjam`),
  ADD KEY `kodeBuku` (`kodeBuku`),
  ADD KEY `NIM` (`NIM`);

--
-- Indeks untuk tabel `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`username`);

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `tkembali`
--
ALTER TABLE `tkembali`
  ADD CONSTRAINT `tkembali_ibfk_1` FOREIGN KEY (`kodeBuku`) REFERENCES `tbuku` (`kodeBuku`),
  ADD CONSTRAINT `tkembali_ibfk_2` FOREIGN KEY (`NIM`) REFERENCES `tanggota` (`NIM`);

--
-- Ketidakleluasaan untuk tabel `tpinjam`
--
ALTER TABLE `tpinjam`
  ADD CONSTRAINT `tpinjam_ibfk_1` FOREIGN KEY (`kodeBuku`) REFERENCES `tbuku` (`kodeBuku`),
  ADD CONSTRAINT `tpinjam_ibfk_2` FOREIGN KEY (`NIM`) REFERENCES `tanggota` (`NIM`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
