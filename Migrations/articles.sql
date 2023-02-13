
-- -----------------------------------------------------
-- Table `articles`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `articles`;

CREATE TABLE `articles` (
    `id`                    int NOT NULL AUTO_INCREMENT,
    `sources_id`            int DEFAULT NULL,
    `title`                 varchar(255) DEFAULT NULL,
    `detail`                text DEFAULT NULL,
    `image_url`             varchar(255) DEFAULT NULL,
    `url`                   varchar(255) DEFAULT NULL,
    `shorter_url`           varchar(255) DEFAULT NULL,
    `status`                enum('NEW', 'PROCESSED', 'POSTED', 'ERROR', 'NO_TAG_MATCH') COLLATE utf8_unicode_ci DEFAULT 'NEW',
    `date_published`        datetime DEFAULT NULL,
    `date_updated`          datetime DEFAULT NULL,
    `date_created`          datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `url` (`url`) USING BTREE,
    UNIQUE KEY `shorter_url` (`shorter_url`) USING BTREE,
    UNIQUE KEY `title` (`title`) USING BTREE
) ENGINE=InnoDB;

DROP TRIGGER IF EXISTS `articles_create`;
CREATE TRIGGER `articles_create` BEFORE INSERT ON `articles` FOR EACH ROW SET NEW.date_created = NOW();

DROP TRIGGER IF EXISTS `articles_update`;
CREATE TRIGGER `articles_update` BEFORE UPDATE ON `articles` FOR EACH ROW SET NEW.date_updated = NOW();
