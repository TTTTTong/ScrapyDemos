DROP TABLE IF EXISTS `regal_holder`;
CREATE TABLE `regal_holder` (
  `currency` varchar(255) NOT NULL ,
  `rank` tinyint(3) NOT NULL,
  `address` varchar(255) NOT NULL,
  `quantity` float(20,10) NOT NULL,
  `per` FLOAT (6,6) NOT NULL,
  PRIMARY KEY (`currency`, `rank`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `unusual`;
CREATE TABLE `unusual`(
    `currency` varchar(255) NOT NULL ,
    `txid` varchar(255) NOT NULL,
    `quantity` float NOT NULL,
    `time` bigint(20) NOT NULL ,
    `is_regal` tinyint(1) NOT NULL DEFAULT 0,
    `from_addr` varchar(255) NOT NULL,
    `to_addr` varchar(255) NOT NULL,
    PRIMARY KEY (`currency`, `txid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
