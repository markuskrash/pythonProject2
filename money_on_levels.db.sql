--
-- Файл сгенерирован с помощью SQLiteStudio v3.3.3 в Пн янв 24 00:49:32 2022
--
-- Использованная кодировка текста: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: Money_on_levels
CREATE TABLE Money_on_levels (id PRIMARY KEY, gold_money INT, liver_money INT, bronze_money INT);
INSERT INTO Money_on_levels (id, gold_money, liver_money, bronze_money) VALUES (3, 0, 0, 0);
INSERT INTO Money_on_levels (id, gold_money, liver_money, bronze_money) VALUES (2, 0, 0, 0);
INSERT INTO Money_on_levels (id, gold_money, liver_money, bronze_money) VALUES (1, 1, 0, 0);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
