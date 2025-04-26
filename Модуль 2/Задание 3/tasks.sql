-- модели принтеров с максимальной ценой
SELECT model, price FROM Printer 
WHERE price = (SELECT MAX(price) FROM Printer);

-- Средняя свкорость ПК
SELECT AVG(speed) FROM PC;

-- Производители, у которых есть ПК, но не ноутбуки
SELECT DISTINCT maker FROM Product
WHERE type = 'PC' AND maker NOT IN (
    SELECT maker FROM Product WHERE type = 'Laptop'
);

-- Загрязнение датасета
INSERT INTO PC
    SELECT ROW_NUMBER() OVER() + 1857,
           model, speed, ram, hdd, cd, price
    FROM PC LIMIT 57
;

-- Нахождение дубликатов
SELECT model
FROM (
    SELECT model, ROW_NUMBER() OVER(PARTITION BY model) AS rn 
    FROM PC 
) 
WHERE rn > 1; 

-- Изменение столбца
ALTER TABLE Product ALTER COLUMN price TYPE VARCHAR(10);

-- ПК и ноутбуки с ram равной 64 и ценой больше 500
SELECT model, price, ram FROM (
    SELECT model, price, ram FROM PC
    UNION
    SELECT model, price, ram FROM Laptop
)
WHERE price > 500 AND ram = 64;
