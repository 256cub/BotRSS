
-- -----------------------------------------------------
-- Table `telegram_channels_has_tags`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `telegram_channels_has_tags`;

CREATE TABLE `telegram_channels_has_tags` (
    `id`                    int NOT NULL AUTO_INCREMENT,
    `telegram_channels_id`  int DEFAULT NULL,
    `tags_id`               int DEFAULT NULL,
    `date_updated`          datetime DEFAULT NULL,
    `date_created`          datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    INDEX `fk_telegram_channels_has_tags_telegram_channels1_idx` (`telegram_channels_id` ASC),
    CONSTRAINT `fk_telegram_channels_has_tags_telegram_channels1` FOREIGN KEY (`telegram_channels_id`) REFERENCES `telegram_channels` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
    INDEX `fk_telegram_channels_has_tags_tags1_idx` (`tags_id` ASC),
    CONSTRAINT `fk_telegram_channels_has_tags_tags1` FOREIGN KEY (`tags_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB;

DROP TRIGGER IF EXISTS `telegram_channels_has_tags_create`;
CREATE TRIGGER `telegram_channels_has_tags_create` BEFORE INSERT ON `telegram_channels_has_tags` FOR EACH ROW SET NEW.date_created = NOW();

DROP TRIGGER IF EXISTS `telegram_channels_has_tags_update`;
CREATE TRIGGER `telegram_channels_has_tags_update` BEFORE UPDATE ON `telegram_channels_has_tags` FOR EACH ROW SET NEW.date_updated = NOW();
