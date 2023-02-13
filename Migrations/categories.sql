
-- -----------------------------------------------------
-- Table `categories`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `categories`;

CREATE TABLE `categories` (
    `id`                int NOT NULL AUTO_INCREMENT,
    `name`              varchar(255) DEFAULT NULL,
    `status`            enum('INACTIVE', 'ACTIVE') DEFAULT 'ACTIVE',
    `date_updated`      datetime DEFAULT NULL,
    `date_created`      datetime DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;

DROP TRIGGER IF EXISTS `categories_create`;
CREATE TRIGGER `categories_create` BEFORE INSERT ON `categories` FOR EACH ROW SET NEW.date_created = NOW();

DROP TRIGGER IF EXISTS `categories_update`;
CREATE TRIGGER `categories_update` BEFORE UPDATE ON `categories` FOR EACH ROW SET NEW.date_updated = NOW();
