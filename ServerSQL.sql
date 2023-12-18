-- 创建FLIGHTS表
CREATE TABLE FLIGHTS (
    id SERIAL,
    flightNum VARCHAR(255) NOT NULL,
    price INT NOT NULL,
    numSeats INT NOT NULL,
    numAvail INT NOT NULL,
    FromCity VARCHAR(255) NOT NULL,
    ArivCity VARCHAR(255) NOT NULL,
    PRIMARY KEY (flightNum)
);

-- 创建HOTELS表
CREATE TABLE HOTELS (
    location VARCHAR(255) NOT NULL,
    price INT NOT NULL,
    numRooms INT NOT NULL,
    numAvail INT NOT NULL,
    PRIMARY KEY (location)
);

-- 创建BUS表
CREATE TABLE BUS (
    id SERIAL,
    location VARCHAR(255) NOT NULL,
    price INT NOT NULL,
    numBus INT NOT NULL,
    numAvail INT NOT NULL,
    PRIMARY KEY (location)
);

-- 创建CUSTOMERS表
CREATE TABLE CUSTOMERS (
    custName VARCHAR(255) NOT NULL,
    custID INT NOT NULL,
    PRIMARY KEY (custName)
);

-- 创建RESERVATIONS表
CREATE TABLE RESERVATIONS (
    resvKey SERIAL,
    custName VARCHAR(255) NOT NULL,
    resvType INT NOT NULL,
    flightId INT,
    busId INT,
    hotelLocation VARCHAR(255),
    PRIMARY KEY (resvKey),
    FOREIGN KEY (custName) REFERENCES CUSTOMERS(custName)
);

INSERT INTO FLIGHTS (flightNum, price, numSeats, numAvail, FromCity, ArivCity)
VALUES 
('F001', 500, 200, 200, 'Beijing', 'Shanghai'),
('F002', 300, 150, 150, 'Shanghai', 'Beijing'),
('F003', 400, 180, 180, 'Beijing', 'Chengdu'),
('F004', 350, 160, 160, 'Chengdu', 'Beijing'),
('F005', 450, 170, 170, 'Beijing', 'Guangzhou'),
('F006', 420, 165, 165, 'Guangzhou', 'Beijing'),
('F007', 480, 175, 175, 'Beijing', 'Xian'),
('F008', 460, 168, 168, 'Xian', 'Beijing'),
('F009', 500, 200, 200, 'Shanghai', 'Chengdu'),
('F010', 300, 150, 150, 'Chengdu', 'Shanghai'),
('F011', 400, 180, 180, 'Shanghai', 'Guangzhou'),
('F012', 350, 160, 160, 'Guangzhou', 'Shanghai'),
('F013', 450, 170, 170, 'Shanghai', 'Xian'),
('F014', 420, 165, 165, 'Xian', 'Shanghai'),
('F015', 480, 175, 175, 'Chengdu', 'Guangzhou'),
('F016', 460, 168, 168, 'Guangzhou', 'Chengdu'),
('F017', 500, 200, 200, 'Chengdu', 'Xian'),
('F018', 300, 150, 150, 'Xian', 'Chengdu'),
('F019', 400, 180, 180, 'Guangzhou', 'Xian'),
('F020', 350, 160, 160, 'Xian', 'Guangzhou');

INSERT INTO HOTELS (location, price, numRooms, numAvail)
VALUES 
('Beijing', 1000, 50, 50),
('Shanghai', 800, 60, 60),
('Xian', 1200, 40, 40),
('Guangzhou', 900, 70, 70),
('Chengdu', 1100, 55, 55);

INSERT INTO BUS (location, price, numBus, numAvail)
VALUES 
('Beijing', 50, 20, 20),
('Shanghai', 45, 25, 25),
('Guangzhou', 55, 15, 15),
('Chengdu', 40, 30, 30),
('Xian', 60, 10, 10);

INSERT INTO CUSTOMERS (custName, custID)
VALUES 
('Alice', 1001),
('Bob', 1002),
('Charlie', 1003),
('David', 1004),
('Eve', 1005),
('Frank', 1006),
('Grace', 1007),
('Helen', 1008),
('Ian', 1009),
('Jane', 1010);

INSERT INTO RESERVATIONS (custName, resvType, flightId, busId, hotelLocation)
VALUES 
('Alice', 1, 0, NULL, NULL),  -- 假设 Alice 预订了 ID 为 1 的航班
('Alice', 3, NULL, 1, NULL),  -- 假设 Alice 预订了从北京出发的巴士
('Alice', 2, NULL, NULL, 'Beijing');  -- 假设 Alice 在北京预订了酒店