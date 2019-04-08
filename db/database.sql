SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;


--
-- Base de donnĂ©es :  `station-meteo`
--

-- --------------------------------------------------------


DROP DATABASE IF EXISTS `station-meteo`;
        
CREATE DATABASE IF NOT EXISTS `station-meteo`;

USE `station-meteo`;
        

-- --------------------------------------------------------

--
-- Structure de la table `sensor`
--

DROP TABLE IF EXISTS `sensor`;
CREATE TABLE IF NOT EXISTS `sensor` (
  `id_sensor` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(55) NOT NULL,
  `ID` int(11) NOT NULL,
  `Mac` varchar(17) NOT NULL,
  PRIMARY KEY (`id_sensor`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;


-- --------------------------------------------------------

--
-- Structure de la table `data_sensor`
--

DROP TABLE IF EXISTS `data_sensor`;
CREATE TABLE IF NOT EXISTS `data_sensor` (
  `id_data_sensor` int(11) NOT NULL AUTO_INCREMENT,
  `battery` int(11) NOT NULL,
  `temperature` decimal(10,2) NOT NULL,
  `humidity` decimal(10,2) NOT NULL,
  `id_sensor` int(11) NOT NULL,
  PRIMARY KEY (`id_data_sensor`),
  KEY `id_sensor` (`id_sensor`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;