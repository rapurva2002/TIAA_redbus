-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 04, 2023 at 10:19 AM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bus`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`id`, `username`, `password`, `email`) VALUES
(2, 'apurva', 'password', 'apurva@gmail.com'),
(3, 'sample', 'sample', 'sample@gmail.com'),
(4, 'sidharth', 'pass', 'sidharth.vn@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

CREATE TABLE `booking` (
  `boarding` text NOT NULL,
  `destination` text NOT NULL,
  `departing` date NOT NULL,
  `seat_type` text NOT NULL,
  `adults` int(11) NOT NULL,
  `children` int(11) NOT NULL,
  `travel_class` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `booking`
--

INSERT INTO `booking` (`boarding`, `destination`, `departing`, `seat_type`, `adults`, `children`, `travel_class`) VALUES
('mumbai', 'pune', '0000-00-00', 'window', 1, 0, 'sleeper'),
('mumbai', 'pune', '2023-06-12', 'window', 1, 0, 'sleeper'),
('mumbai', 'pune', '2023-05-04', 'window', 3, 0, 'business'),
('banglore', 'hyderabad', '2023-05-13', 'window', 3, 0, 'economy'),
('humpi', 'banglore', '2023-05-12', 'Window', 5, 3, 'economy'),
('pune', 'ratnagiri', '2023-05-13', 'Window', 1, 0, 'Sitting'),
('mumbai', 'pune', '2023-05-12', 'Window', 1, 0, 'Sitting');

-- --------------------------------------------------------

--
-- Table structure for table `registration`
--

CREATE TABLE `registration` (
  `name` text NOT NULL,
  `dob` text NOT NULL,
  `email` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `mobilenumber` bigint(10) NOT NULL,
  `gender` text NOT NULL,
  `idtype` text NOT NULL,
  `idnumber` bigint(50) NOT NULL,
  `authority` text NOT NULL,
  `issuedstate` text NOT NULL,
  `issueddate` text NOT NULL,
  `expirydate` text NOT NULL,
  `addresstype` text NOT NULL,
  `nationality` text NOT NULL,
  `state` text NOT NULL,
  `district` text NOT NULL,
  `city` text NOT NULL,
  `pincode` bigint(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `registration`
--

INSERT INTO `registration` (`name`, `dob`, `email`, `password`, `mobilenumber`, `gender`, `idtype`, `idnumber`, `authority`, `issuedstate`, `issueddate`, `expirydate`, `addresstype`, `nationality`, `state`, `district`, `city`, `pincode`) VALUES
('Mayur Sampat Bhore', '2023-05-02', 'mayur.sb@somaiya.edu', 'Mayur123456789', 8779944859, 'Male', 'Driving License', 12345678, 'Indian Government ', 'Maharashtra', '2023-05-01', '2023-05-02', 'Permanent', 'Indian', 'Maharashtra', 'Mumbai', 'Mumbai', 400075),
('Apurva', '2002-10-16', 'rapurva@gmail.com', 'password', 498439549, 'Female', 'aadhar', 348943, 'udai', 'dfdfn', '2019-12-12', '2029-12-12', 'fgnldf', 'ndsds', 'dsj', 'fskj', 'fdfvfkjf', 34983);

-- --------------------------------------------------------

--
-- Table structure for table `sample`
--

CREATE TABLE `sample` (
  `uid` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(150) NOT NULL,
  `pass` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `sample`
--

INSERT INTO `sample` (`uid`, `name`, `email`, `pass`) VALUES
(2147483647, 'Jace', 'jace123@gmail.com', 'jace123'),
(2147483647, 'Clary', 'clary.h@gmail.com', 'clary212'),
(2147483647, 'Kavya', 'kavyab123@gmail.com', 'kavsss');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
