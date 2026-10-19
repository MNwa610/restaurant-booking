-- ==========================================
-- Restaurant Booking: структура базы данных
-- ==========================================

CREATE TABLE IF NOT EXISTS tables (
    number INTEGER PRIMARY KEY,
    capacity INTEGER NOT NULL,
    location TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY,
    table_number INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    booking_date TEXT NOT NULL,
    is_cancelled INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (table_number) REFERENCES tables(number),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
