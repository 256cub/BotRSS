
-- -----------------------------------------------------
-- Table `telegram_posts`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `telegram_posts`;

CREATE TABLE `telegram_posts` (
    `id`                    int NOT NULL AUTO_INCREMENT,
    `telegram_channels_id`  int DEFAULT NULL,
    `articles_id`           int DEFAULT NULL,
    `message_id`            int DEFAULT NULL,
    `date_updated`          datetime DEFAULT NULL,
    `date_created`          datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    INDEX `fk_telegram_posts_telegram_channels1_idx` (`telegram_channels_id` ASC),
    CONSTRAINT `fk_telegram_posts_telegram_channels1` FOREIGN KEY (`telegram_channels_id`) REFERENCES `telegram_channels` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
    INDEX `fk_telegram_posts_articles1_idx` (`articles_id` ASC),
    CONSTRAINT `fk_telegram_posts_articles1` FOREIGN KEY (`articles_id`) REFERENCES `articles` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB;

DROP TRIGGER IF EXISTS `telegram_posts_create`;
CREATE TRIGGER `telegram_posts_create` BEFORE INSERT ON `telegram_posts` FOR EACH ROW SET NEW.date_created = NOW();

DROP TRIGGER IF EXISTS `telegram_posts_update`;
CREATE TRIGGER `telegram_posts_update` BEFORE UPDATE ON `telegram_posts` FOR EACH ROW SET NEW.date_updated = NOW();
