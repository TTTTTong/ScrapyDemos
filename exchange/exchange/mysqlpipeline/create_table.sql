DROP TABLE IF EXISTS `regal_holder`;
CREATE TABLE `regal_holder` (
  `currency` varchar(32) NOT NULL ,
  `rank` tinyint(3) NOT NULL,
  `address` varchar(255) NOT NULL,
  `quantity` float(20,10) NOT NULL,
  `per` FLOAT (6,6) NOT NULL,
  PRIMARY KEY (`currency`, `rank`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `currency_chain_info`;
CREATE TABLE `currency_chain_info`(
     `currency` varchar(32) NOT NULL ,
     `holder_count` INT DEFAULT 0,
     `trans_count` INT DEFAULT 0,
     `24h_trans` INT DEFAULT 0,
     `24h_price` FLOAT DEFAULT 0,
     `concentration_10` FLOAT (10,10),
     `concentration_50` FLOAT (10,10),
     `concentration_100` FLOAT (10,10),
     PRIMARY KEY (`currency`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `unusual`;
CREATE TABLE `unusual`(
    `currency` varchar(32) NOT NULL ,
    `txid` varchar(128) NOT NULL,
    `quantity` float NOT NULL,
    `time` bigint(20) NOT NULL ,
    `is_regal` tinyint(1) NOT NULL DEFAULT 0,
    `from_addr` varchar(255) NOT NULL,
    `to_addr` varchar(255) NOT NULL,
    PRIMARY KEY (`currency`, `txid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `token_info`;
CREATE TABLE `token_info`(
    `currency` VARCHAR (32) NOT NULL ,
    `contract` VARCHAR (255) NOT NULL ,
    PRIMARY KEY (`currency`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE if EXISTS `ip_list`;
CREATE TABLE  `ip_list`(
    `ip` VARCHAR (255) NOT NULL ,
    PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;