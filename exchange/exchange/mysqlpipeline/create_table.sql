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
    `quantity` float(11,8) NOT NULL,
    `time` TIMESTAMP(6) NOT NULL ,
    `is_regal` tinyint(1) NOT NULL DEFAULT 0,
    `from` varchar(255) NOT NULL,
    `to` varchar(255) NOT NULL,
    PRIMARY KEY (`currency`, `txid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
