
CREATE TABLE `card_rulings` (
  `id` INTEGER PRIMARY KEY,
  `card_def_id` INTEGER,
  `ruling_text` TEXT
);

CREATE TABLE `card_types` (
  `id` INTEGER PRIMARY KEY,
  `type` TEXT
);

CREATE TABLE `cards` (
  `id` INTEGER PRIMARY KEY,
  `edition_id` INTEGER,
  `name` TEXT,
);

CREATE TABLE `card_definition` (
  `id` INTEGER PRIMARY KEY,
  `card_id` INTEGER,
  `cast_cost` TEXT,
  `abilities` TEXT,
  `oracle` TEXT,
  `flavor` TEXT,
  `double_id` INTEGER,
  `illustrator_id` INTEGER,
  `rarity` TEXT,
  `power` TEXT,
  `toughness` TEXT,
  `price_low` REAL,
  `price_med` REAL,
  `price_high` REAL
);

CREATE TABLE `editions` (
  `id` INTEGER PRIMARY KEY,
  `edition` TEXT
);

CREATE TABLE `illustrators` (
  `id` INTEGER PRIMARY KEY,
  `name` TEXT
);

CREATE TABLE `legalities` (
  `id` INTEGER PRIMARY KEY, 
  `version` TEXT
);

CREATE TABLE `x_cards_types` (
  `card_id` INTEGER,
  `type_id` INTEGER,
  `sequence` INTEGER
);

CREATE TABLE `x_legalities` (
  `card_id` INTEGER,
  `legality_id` INTEGER
);
