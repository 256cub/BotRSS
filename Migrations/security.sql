
-- -----------------------------------------------------
-- Table `security`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `security`;

CREATE TABLE `security` (
    `id`                int NOT NULL AUTO_INCREMENT,
    `username`          varchar(255) DEFAULT NULL,
    `first_name`        varchar(255) DEFAULT NULL,
    `last_name`         varchar(255) DEFAULT NULL,
    `user_id`           int DEFAULT NULL,
    `language_code`     varchar(255) DEFAULT NULL,
    `is_bot`            tinyint(1) DEFAULT NULL,
    `date_updated`      datetime DEFAULT NULL,
    `date_created`      datetime DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;

DROP TRIGGER IF EXISTS `security_create`;
CREATE TRIGGER `security_create` BEFORE INSERT ON `security` FOR EACH ROW SET NEW.date_created = NOW();

DROP TRIGGER IF EXISTS `security_update`;
CREATE TRIGGER `security_update` BEFORE UPDATE ON `security` FOR EACH ROW SET NEW.date_updated = NOW();