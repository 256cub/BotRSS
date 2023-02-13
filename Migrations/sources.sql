
-- -----------------------------------------------------
-- Table `sources`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sources`;

CREATE TABLE `sources` (
    `id`                    int NOT NULL AUTO_INCREMENT,
    `rss_url`               varchar(255) DEFAULT NULL,
    `status`                enum('ACTIVE', 'INACTIVE') COLLATE utf8_unicode_ci DEFAULT 'ACTIVE',
    `date_updated`          datetime DEFAULT NULL,
    `date_created`          datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `rss_url` (`rss_url`) USING BTREE
) ENGINE=InnoDB;

DROP TRIGGER IF EXISTS `sources_create`;
CREATE TRIGGER `sources_create` BEFORE INSERT ON `sources` FOR EACH ROW SET NEW.date_created = NOW();

DROP TRIGGER IF EXISTS `sources_update`;
CREATE TRIGGER `sources_update` BEFORE UPDATE ON `sources` FOR EACH ROW SET NEW.date_updated = NOW();
