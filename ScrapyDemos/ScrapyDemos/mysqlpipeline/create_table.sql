DROP TABLE IF EXISTS `douban_top`;
CREATE TABLE `douban_top` (
  `rank` int(11) NOT NULL ,
  `movie_name` varchar(255) DEFAULT NULL,
  `score` varchar(255) DEFAULT NULL,
  `score_num` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`rank`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;