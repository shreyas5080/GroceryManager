
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_fname VARCHAR(100) NOT NULL,
    user_lname VARCHAR(100) NOT NULL,
    user_email VARCHAR(255) UNIQUE NOT NULL,
    user_password VARCHAR(255) NOT NULL
);
CREATE TABLE groceryitems (
    item_id SERIAL PRIMARY KEY,
    itemname VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,
    user_email VARCHAR(255) NOT NULL,

    FOREIGN KEY (user_email)
    REFERENCES users(user_email)
    ON DELETE CASCADE
);
CREATE TABLE storing_temp_otp (
	id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    otp VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);