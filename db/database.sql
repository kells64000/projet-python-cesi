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
  `Mac` varchar(17) NOT NULL
  PRIMARY KEY (`id_sensor`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;


-- --------------------------------------------------------

--
-- Structure de la table `data_sensor`
--

DROP TABLE IF EXISTS `data_sensor`;
CREATE TABLE IF NOT EXISTS `data_sensor` (
  `id_data_sensor` int(11) NOT NULL AUTO_INCREMENT,
  `date_releve` datetime not null,
  `battery` int(11),
  `temperature` decimal(10,2),
  `humidity` decimal(10,2),
  `detected_signal` boolean NOT NULL,
  `id_sensor` int(11) NOT NULL,
  PRIMARY KEY (`id_data_sensor`),
  KEY `id_sensor` (`id_sensor`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `weather_api`;
CREATE TABLE IF NOT EXISTS `weather_api` (
  `id_weather_api` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(55) NOT NULL,
  PRIMARY KEY (`id_weather_api`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `data_weather_api`;
CREATE TABLE IF NOT EXISTS `data_weather_api` (
  `id_data_weather_api` int(11) NOT NULL AUTO_INCREMENT,
  `date_releve` datetime not null,
  `temperature` decimal(10,2),
  `humidity` decimal(10,2),
  `detected_signal` boolean NOT NULL,
  `id_weather_api` int(11) NOT NULL,
  PRIMARY KEY (`id_data_weather_api`),
  KEY `id_sensor` (`id_weather_api`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
