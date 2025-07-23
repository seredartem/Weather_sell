

CREATE TABLE Account(
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(80) NOT NULL,
    balance DECIMAL(6,2) NOT NULL DEFAULT(0) CHECK(balance >= 0),
    requests INT NOT NULL DEFAULT(0) CHECK(requests >= 0 and requests <= 10),
    created_at TIMESTAMP DEFAULT(CURRENT_TIMESTAMP)
)


CREATE TABLE Transaction(
    id INT PRIMARY KEY AUTO_INCREMENT,
    money DECIMAL(6,2) NOT NULL,
    reason VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT(CURRENT_TIMESTAMP),

    account_id INT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES Account(id)
)

CREATE TABLE RequestLog(
    id INT PRIMARY KEY AUTO_INCREMENT,
    city VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT(CURRENT_TIMESTAMP),

    account_id INT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES Account(id)
)
