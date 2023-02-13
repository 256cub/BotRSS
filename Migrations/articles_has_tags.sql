
-- -----------------------------------------------------
-- Table `articles_has_tags`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `articles_has_tags`;

CREATE TABLE `articles_has_tags` (
    `id`                int NOT NULL AUTO_INCREMENT,
    `articles_id`       int DEFAULT NULL,
    `tags_id`           int DEFAULT NULL,
    `date_updated`      datetime DEFAULT NULL,
    `date_created`      datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    INDEX `fk_articles_has_tags_articles1_idx` (`articles_id` ASC),
    CONSTRAINT `fk_articles_has_tags_articles1` FOREIGN KEY (`articles_id`) REFERENCES `articles` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
    INDEX `fk_articles_has_tags_tags1_idx` (`tags_id` ASC),
    CONSTRAINT `fk_articles_has_tags_tags1` FOREIGN KEY (`tags_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB;

DROP TRIGGER IF EXISTS `articles_has_tags_create`;
CREATE TRIGGER `articles_has_tags_create` BEFORE INSERT ON `articles_has_tags` FOR EACH ROW SET NEW.date_created = NOW();

DROP TRIGGER IF EXISTS `articles_has_tags_update`;
CREATE TRIGGER `articles_has_tags_update` BEFORE UPDATE ON `articles_has_tags` FOR EACH ROW SET NEW.date_updated = NOW();
