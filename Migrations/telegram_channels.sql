
-- -----------------------------------------------------
-- Table `telegram_channels`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `telegram_channels`;

CREATE TABLE `telegram_channels` (
    `id`                    int NOT NULL AUTO_INCREMENT,
    `username`              varchar(255) DEFAULT NULL,
    `total_posts`           int DEFAULT NULL,
    `status`                enum('ACTIVE', 'INACTIVE') COLLATE utf8_unicode_ci DEFAULT 'ACTIVE',
    `date_updated`          datetime DEFAULT NULL,
    `date_created`          datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `username` (`username`) USING BTREE
) ENGINE=InnoDB;

DROP TRIGGER IF EXISTS `telegram_channels_create`;
CREATE TRIGGER `telegram_channels_create` BEFORE INSERT ON `telegram_channels` FOR EACH ROW SET NEW.date_created = NOW();

DROP TRIGGER IF EXISTS `telegram_channels_update`;
CREATE TRIGGER `telegram_channels_update` BEFORE UPDATE ON `telegram_channels` FOR EACH ROW SET NEW.date_updated = NOW();
