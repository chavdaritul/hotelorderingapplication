-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 11, 2021 at 10:00 AM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hotel_ordering_application`
--

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `id` int(11) NOT NULL,
  `name` varchar(225) NOT NULL,
  `emailid` varchar(225) NOT NULL,
  `address` varchar(225) NOT NULL,
  `phone` varchar(225) NOT NULL,
  `password` varchar(225) NOT NULL,
  `dob` date DEFAULT NULL,
  `document_verified` varchar(225) NOT NULL DEFAULT 'Not-Uploaded'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`id`, `name`, `emailid`, `address`, `phone`, `password`, `dob`, `document_verified`) VALUES
(8, 'demo', 'demo@demo.com', 'Kasavanahalli', '1234567890', '$2b$12$Dz39JbAnS6z7zjEQm70V6OXza72K5f0a8230/FqI8L8STctDIOC7W', NULL, 'Not-Uploaded'),
(11, 'test', 'demo@demo.com', 'test123', '1425367890', '$2b$12$qgLFs5yucZ8cacraV0YckOHBmBJmDLK.ddt2mQb5ELQx.8aHDMs3u', NULL, 'Not-Uploaded'),
(12, 'demo1', 'demo@gmail.com', '', '', '$2b$12$VIlPB4Ma9Xg08Nfxm8K9H.a7B7W4tE0raHHcP5z6HQpDUglC2PvcO', NULL, 'Not-Uploaded'),
(13, 'ritul', 'ritul@gmail.com', 'Gandhinagar', '9714710162', '$2b$12$4t1p3QzWs2QkdVInv5jIrOEcwT92jlDZOawS4hHGtDAIlk3oL/tUm', NULL, 'Verified'),
(14, 'ritulchavda', 'ritulchavda@gmail.com', 'Bengaluru, Karnataka', '1234567890', '$2b$12$twILL5/XnjZ6N/czBvFpc.9dXkpoP/q8QW8klKqr6bxHWyEcIV0U2', '2021-12-09', 'Verified');

-- --------------------------------------------------------

--
-- Table structure for table `menu`
--

CREATE TABLE `menu` (
  `pid` int(11) NOT NULL,
  `name` varchar(225) NOT NULL,
  `image` varchar(225) NOT NULL,
  `category` varchar(225) NOT NULL,
  `price` int(11) NOT NULL,
  `description` varchar(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `menu`
--

INSERT INTO `menu` (`pid`, `name`, `image`, `category`, `price`, `description`) VALUES
(1, 'Pasta', 'pasta.jpg', 'starter', 150, 'Pasta is a type of food typically made from an unleavened dough of wheat flour mixed with water or eggs, and formed into sheets or other shapes, then cooked by boiling or baking.'),
(2, 'Pizza', 'pizza.jpg', 'main', 350, 'Pizza is a dish of Italian origin consisting of a usually round, flat base of leavened wheat-based dough topped with tomatoes, cheese, and often various other ingredients.'),
(3, 'Dosa', 'dosa.jpg', 'main', 200, 'A dosa is a thin pancake or crepe originating from South India'),
(4, 'Tomato Soup', 'tomato_soup.jpg', 'starter', 100, 'Tomato soup is a soup with tomatoes as the primary ingredient.'),
(5, 'Salad', 'salad.jpg', 'starter', 100, 'A salad is a dish consisting of mixed pieces of food, typically with at least one raw ingredient.'),
(6, 'Pav Bhaji', 'pav_bhaji.jpg', 'main', 200, 'Pav bhaji is a fast food dish from India consisting of a thick vegetable curry served with a soft bread roll.'),
(7, 'Brownie', 'brownie.jpg', 'dessert', 100, 'A chocolate brownie or simply a brownie is a square or rectangular chocolate baked confection.'),
(8, 'Cup Cakes', 'cup-cake.jpg', 'dessert', 50, 'A cupcake is a small cake designed to serve one person, which may be baked in a small thin paper or aluminum cup.'),
(9, 'Donuts', 'donuts.jpg', 'dessert', 50, 'A doughnut or donut is a type of leavened fried dough.'),
(10, 'Coca Cola', 'coca-cola.jpg', 'beverages', 50, 'A drink is a liquid intended for human consumption.'),
(11, 'Ice Cream', 'ice-cream.jpg', 'dessert', 50, 'Ice cream is a sweetened frozen food typically eaten as a snack or dessert.'),
(12, 'Paneer Roti', 'paneer-rice-roti.jpg', 'main', 200, 'Paneer paratha is a popular North Indian flatbread made with whole wheat flour dough and stuffed with savory, spiced, grated paneer.'),
(13, 'Pepsi', 'pepsi.jpg', 'beverages', 50, 'A drink is a liquid intended for human consumption.'),
(14, 'Cold Drinks', 'cold-drinks.png', 'beverages', 100, 'A drink is a liquid intended for human consumption.'),
(15, 'Smoothies', 'smoothies.png', 'beverages', 100, 'A smoothie or smoothie is a drink made by puréeing fruit and vegetables in a blender.'),
(16, 'Thali', 'thali.jpg', 'main', 200, 'Indian food consisting of different kinds of curry and more.'),
(17, 'Lasagne', 'lasagna.png', 'main', 150, 'Lasagne are a type of pasta, possibly one of the oldest types, made of very wide, flat sheets.');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`pid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `menu`
--
ALTER TABLE `menu`
  MODIFY `pid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
