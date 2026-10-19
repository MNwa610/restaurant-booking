-- Назначение запроса: список всех столиков
SELECT
    number,
    capacity,
    location
FROM tables
ORDER BY number;

-- Назначение запроса: список всех пользователей
SELECT
    id,
    name,
    email
FROM users
ORDER BY name;

-- Назначение запроса: столики с вместимостью не меньше 4
SELECT
    number,
    capacity,
    location
FROM tables
WHERE capacity >= 4
ORDER BY capacity;

-- Назначение запроса: список активных бронирований
SELECT
    id,
    table_number,
    user_id,
    booking_date
FROM bookings
WHERE is_cancelled = 0
ORDER BY booking_date;

-- Назначение запроса: столики у окна
SELECT
    number,
    capacity,
    location
FROM tables
WHERE location = 'У окна'
ORDER BY number;

-- Назначение запроса: активные бронирования со столиком и пользователем
SELECT
    bookings.id,
    bookings.booking_date,
    tables.number AS table_number,
    tables.capacity,
    tables.location,
    users.name AS user_name,
    users.email
FROM bookings
JOIN tables
    ON bookings.table_number = tables.number
JOIN users
    ON bookings.user_id = users.id
WHERE bookings.is_cancelled = 0
ORDER BY bookings.booking_date;

-- Назначение запроса: отменённые бронирования со столиком и пользователем
SELECT
    bookings.id,
    bookings.booking_date,
    tables.number AS table_number,
    users.name AS user_name,
    users.email
FROM bookings
JOIN tables
    ON bookings.table_number = tables.number
JOIN users
    ON bookings.user_id = users.id
WHERE bookings.is_cancelled = 1
ORDER BY bookings.booking_date;

-- Назначение запроса: свободные столики на выбранную дату
SELECT
    tables.number,
    tables.capacity,
    tables.location
FROM tables
WHERE tables.number NOT IN (
    SELECT bookings.table_number
    FROM bookings
    WHERE bookings.booking_date = '2026-10-06'
        AND bookings.is_cancelled = 0
)
ORDER BY tables.number;

-- Назначение запроса: количество активных бронирований
SELECT
    COUNT(*) AS bookings_count
FROM bookings
WHERE is_cancelled = 0;

-- Назначение запроса: средняя, минимальная и максимальная вместимость
SELECT
    AVG(capacity) AS avg_capacity,
    MIN(capacity) AS min_capacity,
    MAX(capacity) AS max_capacity
FROM tables;

-- Назначение запроса: количество активных бронирований по каждому столику
SELECT
    tables.number AS table_number,
    COUNT(bookings.id) AS bookings_count
FROM tables
LEFT JOIN bookings
    ON tables.number = bookings.table_number
    AND bookings.is_cancelled = 0
GROUP BY tables.number
ORDER BY bookings_count DESC;

-- Назначение запроса: количество столиков по расположению
SELECT
    location,
    COUNT(*) AS tables_count
FROM tables
GROUP BY location
ORDER BY tables_count DESC;

-- Назначение запроса: столики хотя бы с одним активным бронированием
SELECT
    tables.number AS table_number,
    COUNT(bookings.id) AS bookings_count
FROM tables
JOIN bookings
    ON tables.number = bookings.table_number
WHERE bookings.is_cancelled = 0
GROUP BY tables.number
HAVING COUNT(bookings.id) >= 1
ORDER BY bookings_count DESC;

-- Назначение запроса: расположения, в которых больше одного столика
SELECT
    location,
    COUNT(*) AS tables_count
FROM tables
GROUP BY location
HAVING COUNT(*) > 1
ORDER BY tables_count DESC;

-- Назначение запроса: карточка столика по номеру
SELECT
    number,
    capacity,
    location
FROM tables
WHERE number = 1;

-- Назначение запроса: свободность столика на выбранную дату
SELECT
    tables.number
FROM tables
WHERE tables.number = 1
    AND tables.number NOT IN (
        SELECT bookings.table_number
        FROM bookings
        WHERE bookings.booking_date = '2026-10-06'
            AND bookings.is_cancelled = 0
    );

-- Назначение запроса: карточка бронирования со столиком и пользователем
SELECT
    bookings.id,
    bookings.booking_date,
    bookings.is_cancelled,
    tables.number AS table_number,
    users.name AS user_name
FROM bookings
JOIN tables
    ON bookings.table_number = tables.number
JOIN users
    ON bookings.user_id = users.id
WHERE bookings.id = 1;
