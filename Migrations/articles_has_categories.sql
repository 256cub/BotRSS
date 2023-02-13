
-- -----------------------------------------------------
-- Table `articles_has_categories`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `articles_has_categories`;

CREATE TABLE `articles_has_categories` (
    `id`                int NOT NULL AUTO_INCREMENT,
    `articles_id`       int DEFAULT NULL,
    `categories_id`     int DEFAULT NULL,
    `date_updated`      datetime DEFAULT NULL,
    `date_created`      datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    INDEX `fk_articles_has_categories_articles1_idx` (`articles_id` ASC),
    CONSTRAINT `fk_articles_has_categories_articles1` FOREIGN KEY (`articles_id`) REFERENCES `articles` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
    INDEX `fk_articles_has_categories_categories1_idx` (`categories_id` ASC),
    CONSTRAINT `fk_articles_has_categories_categories1` FOREIGN KEY (`categories_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB;

DROP TRIGGER IF EXISTS `articles_has_categories_create`;
CREATE TRIGGER `articles_has_categories_create` BEFORE INSERT ON `articles_has_categories` FOR EACH ROW SET NEW.date_created = NOW();

DROP TRIGGER IF EXISTS `articles_has_categories_update`;
CREATE TRIGGER `articles_has_categories_update` BEFORE UPDATE ON `articles_has_categories` FOR EACH ROW SET NEW.date_updated = NOW();
