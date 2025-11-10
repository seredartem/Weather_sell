

CREATE TABLE Account(
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(250) NOT NULL,
    balance DECIMAL(6,2) NOT NULL DEFAULT(0) CHECK(balance >= 0),
    requests INT NOT NULL DEFAULT(0) CHECK(requests >= 0 and requests <= 10),
    created_at TIMESTAMP DEFAULT(CURRENT_TIMESTAMP)
)

ALTER TABLE Account
    MODIFY email VARCHAR(254),
    MODIFY balance DECIMAL(12,2) NOT NULL DEFAULT 0,
    ADD INDEX ix_account_created_at (created_at)

CREATE TABLE `Transaction`(
    id INT PRIMARY KEY AUTO_INCREMENT,
    money DECIMAL(6,2) NOT NULL,
    reason VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT(CURRENT_TIMESTAMP),

    account_id INT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES Account(id)
)

ALTER TABLE `Transaction`
    MODIFY money DECIMAL(12,2) NOT NULL,
    ADD COLUMN type ENUM('deposite','withdraw') NOT NULL AFTER money,
    ADD COLUMN status ENUM('pending','completed','failed') NOT NULL DEFAULT 'pending' AFTER type,
    ADD UNIQUE KEY transaction_idem (idempotency_key),
    ADD CHECK (money > 0),
    ADD INDEX ix_trx_account_created (account_id, created_at)

CREATE TABLE RequestLog(
    id INT PRIMARY KEY AUTO_INCREMENT,
    city VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT(CURRENT_TIMESTAMP),
    account_id INT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES Account(id)
)

ALTER TABLE RequestLog
    ADD COLUMN temp DECIMAL(5,2) NULL AFTER city,
    ADD COLUMN units ENUM('C','F','K') NOT NULL DEFAULT 'C' AFTER temp,
    ADD UNIQUE KEY request_key (requestkey)

