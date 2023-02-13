
-- -----------------------------------------------------
-- Table `telegram_channels_has_categories`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `telegram_channels_has_categories`;

CREATE TABLE `telegram_channels_has_categories` (
    `id`                    int NOT NULL AUTO_INCREMENT,
    `telegram_channels_id`  int DEFAULT NULL,
    `categories_id`         int DEFAULT NULL,
    `date_updated`          datetime DEFAULT NULL,
    `date_created`          datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    INDEX `fk_telegram_channels_has_categories_telegram_channels1_idx` (`telegram_channels_id` ASC),
    CONSTRAINT `fk_telegram_channels_has_categories_telegram_channels1` FOREIGN KEY (`telegram_channels_id`) REFERENCES `telegram_channels` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
    INDEX `fk_telegram_channels_has_categories_categories1_idx` (`categories_id` ASC),
    CONSTRAINT `fk_telegram_channels_has_categories_categories1` FOREIGN KEY (`categories_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB;

DROP TRIGGER IF EXISTS `telegram_channels_has_categories_create`;
CREATE TRIGGER `telegram_channels_has_categories_create` BEFORE INSERT ON `telegram_channels_has_categories` FOR EACH ROW SET NEW.date_created = NOW();

DROP TRIGGER IF EXISTS `telegram_channels_has_categories_update`;
CREATE TRIGGER `telegram_channels_has_categories_update` BEFORE UPDATE ON `telegram_channels_has_categories` FOR EACH ROW SET NEW.date_updated = NOW();
