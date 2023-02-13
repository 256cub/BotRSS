
-- -----------------------------------------------------
-- Table `tags`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tags`;

CREATE TABLE `tags` (
    `id`                int NOT NULL AUTO_INCREMENT,
    `name`              varchar(255) DEFAULT NULL,
    `status`            enum('INACTIVE', 'ACTIVE') DEFAULT 'ACTIVE',
    `date_updated`      datetime DEFAULT NULL,
    `date_created`      datetime DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;

DROP TRIGGER IF EXISTS `tags_create`;
CREATE TRIGGER `tags_create` BEFORE INSERT ON `tags` FOR EACH ROW SET NEW.date_created = NOW();

DROP TRIGGER IF EXISTS `tags_update`;
CREATE TRIGGER `tags_update` BEFORE UPDATE ON `tags` FOR EACH ROW SET NEW.date_updated = NOW();
