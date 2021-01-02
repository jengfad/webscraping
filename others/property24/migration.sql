CREATE DATABASE `listings` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

use listings;

CREATE TABLE `error_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `notes` text,
  `error_message` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3624 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `properties` (
  `id` int NOT NULL AUTO_INCREMENT,
  `listing_name` text,
  `total_price` double DEFAULT NULL,
  `listing_address` text,
  `listing_title` text,
  `listing_write_up` longtext,
  `bedrooms` int DEFAULT NULL,
  `bathrooms` int DEFAULT NULL,
  `garages` int DEFAULT NULL,
  `garden` tinyint(1) DEFAULT NULL,
  `pets_allowed` tinyint(1) DEFAULT NULL,
  `listing_number` int DEFAULT NULL,
  `property_type` text,
  `street_address` text,
  `list_date` text,
  `floor_area_sqm` float DEFAULT NULL,
  `lot_area_sqm` float DEFAULT NULL,
  `broker_name` text,
  `url` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3624 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `photos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `listing_number` int DEFAULT NULL,
  `original_url` text,
  `filename` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31502 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `interest_points` (
  `id` int NOT NULL AUTO_INCREMENT,
  `listing_number` int DEFAULT NULL,
  `category_name` text,
  `item_name` text,
  `distance_km` float DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=105075 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `photo_files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `listing_number` int DEFAULT NULL,
  `original_url` text,
  `filename` text,
  `file` longblob,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31275 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
