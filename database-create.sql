-- SQL Relational Schema

-- User and its IS-A relationships
CREATE TABLE User(
   ID INT NOT NULL UNIQUE,
   firstname CHAR(20),
   lastname CHAR(20),
   phone_number INT,
   Upassword CHAR(20) NOT NULL,
   email CHAR(20) NOT NULL UNIQUE,
   PRIMARY KEY(ID)
);

CREATE TABLE Customer(
   CID INT NOT NULL UNIQUE,
   Caddress CHAR(20),
   creditcard_no INT,
   PRIMARY KEY (CID),
   FOREIGN KEY (CID) REFERENCES User(ID)
);

CREATE TABLE Admin(
   AID INT NOT NULL UNIQUE,
   ssn INT,
   PRIMARY KEY (AID),
   FOREIGN KEY (AID) REFERENCES User(ID)
);

CREATE TABLE Deliverer(
   DID INT NOT NULL UNIQUE,
   ssn INT,
   PRIMARY KEY (DID),
   FOREIGN KEY (DID) REFERENCES User(ID)
);
	
-- Other Attributes


CREATE TABLE Orders(
   OrderID CHAR(10) NOT NULL,
   Placing_ID INT NOT NULL,
   Delivering_ID INT NOT NULL,
   Containing_ID CHAR(10) NOT NULL,
   order_date DATE,
   delivery_date DATE,
   paid_price INT,
   gift_note CHAR(20),
   PRIMARY KEY (OrderID)
   FOREIGN KEY (Placing_ID) REFERENCES Customer(CID)
   FOREIGN KEY (Delivering_ID) REFERENCES Deliverer(DID)
   FOREIGN KEY (Containing_ID) REFERENCES Flower_arrangement(FID)

);

CREATE TABLE Flower_arrangement(
   FID CHAR(10) NOT NULL UNIQUE,
   Fname CHAR(20),
   price INT,
   quantity INT,
   Ftype CHAR(20),
   Fsize CHAR(20),
   floral_description CHAR(20),
   PRIMARY KEY (FID)
);

CREATE TABLE Discount(
   discount_code CHAR(20) NOT NULL UNIQUE,
   Entering_ID INT NOT NULL,
   discount_perc INT,
   Sdate DATE,
   Edate DATE,
   PRIMARY KEY (discount_code)
   FOREIGN KEY (Entering_ID) REFERENCES Customer(CID)
);
-- Relation Tables

CREATE TABLE enters(
   CID INT NOT NULL,
   discount_code CHAR(20) NOT NULL,
   PRIMARY KEY (CID,discount_code),
   FOREIGN KEY (CID) REFERENCES Customer(CID),
   FOREIGN KEY (discount_code) REFERENCES Discount(discount_code)
);

CREATE TABLE updates(
   OrderID CHAR(10) NOT NULL, -- not unique last change
   DID CHAR(10) NOT NULL,
   Ustatus BOOLEAN,
   PRIMARY KEY (OrderID, DID),
   FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
   FOREIGN KEY (DID) REFERENCES Deliverer(DID)
);

-- Inserting Items

INSERT INTO User (ID, firstname, lastname, phone_number, Upassword, email)
VALUES 
(1, 'John', 'Doe', 1234567890, 'password123', 'john@example.com'),
(2, 'Jane', 'Smith', 9876543210, 'abc123', 'jane@example.com'),
(3, 'Michael', 'Johnson', 5555555555, 'pass123', 'michael@example.com'),
(4, 'Emily', 'Davis', 3333333333, 'emily123', 'emily@example.com'),
(5, 'David', 'Brown', 1111111111, 'davidpass', 'david@example.com'),
(6, 'Sarah', 'Wilson', 5554443333, 'sarahpass', 'sarah@example.com'),
(7, 'Daniel', 'Martinez', 2223334444, 'danielpass', 'daniel@example.com'),
(8, 'Jessica', 'Lee', 7778889999, 'jessicapass', 'jessica@example.com'),
(9, 'Matthew', 'Taylor', 8889990000, 'matthewpass', 'matthew@example.com'),
(10, 'Olivia', 'Garcia', 6667778888, 'oliviapass', 'olivia@example.com'),
(11, 'Ethan', 'Lopez', 4445556666, 'ethanpass', 'ethan@example.com'),
(12, 'Sophia', 'Harris', 3334445555, 'sophiapass', 'sophia@example.com'),
(13, 'Noah', 'Clark', 2223334444, 'noahpass', 'noah@example.com'),
(14, 'Isabella', 'Lewis', 9990001111, 'isabellapass', 'isabella@example.com'),
(15, 'Liam', 'Rodriguez', 1112223333, 'liampass', 'liam@example.com'),
(16, 'Admin', 'Admin', 0000000000, '123', 'customer'),
(17, 'Admin', 'Admin', 0000000001, '123', 'admin'),
(18, 'Admin', 'Admin', 0000000002, '123', 'deliverer');


INSERT INTO Customer (CID, Caddress, creditcard_no)
VALUES 
(1, '123 Main St', 1234567890123456),
(2, '456 Elm St', 9876543210987654),
(3, '789 Oak St', 5555666677778888),
(4, '101 Pine St', 1234123412341234),
(5, '202 Maple St', 9876987698769876),
(16, 'admin', 0000000000000000);


INSERT INTO Admin (AID, ssn)
VALUES 
(6, 123456789),
(7, 987654321),
(8, 555566667),
(9, 111122223),
(10, 999888887),
(17, 000000000);

INSERT INTO Deliverer (DID, ssn)
VALUES 
(11, 987654321),
(12, 123456789),
(13, 555566667),
(14, 111122223),
(15, 999988887),
(18, 000000001);


INSERT INTO Flower_arrangement (FID, Fname, price, quantity, Ftype, Fsize, floral_description)
VALUES 
('FID001', 'Rose Bouquet', 25, 1, 'Rose', 'Small', 'Red roses'),
('FID002', 'Mixed Arrangement', 35, 1, 'Mixed', 'Medium', 'Assorted flowers'),
('FID003', 'Lily Bouquet', 30, 1, 'Lily', 'Large', 'White lilies'),
('FID004', 'Sunflower Arrangement', 40, 1, 'Sunflower', 'Extra Large', 'Yellow sunflowers'),
('FID005', 'Orchid Basket', 50, 1, 'Orchid', 'Large', 'Purple orchids');

INSERT INTO Orders (OrderID, Placing_ID, Delivering_ID, Containing_ID, order_date, delivery_date, paid_price, gift_note)
VALUES 
('ORD001', 1, 11, 'FID001', '2024-04-16', '2024-04-20', 50, 'Happy Birthday!'),
('ORD002', 2, 12, 'FID002', '2024-04-17', '2024-04-21', 75, NULL),
('ORD003', 3, 13, 'FID003', '2024-04-18', '2024-04-22', 100, 'Congratulations!'),
('ORD004', 4, 14, 'FID004', '2024-04-19', '2024-04-23', 150, NULL),
('ORD005', 5, 15, 'FID005', '2024-04-20', '2024-04-24', 200, 'Happy Anniversary!');

INSERT INTO Discount (discount_code, Entering_ID, discount_perc, Sdate, Edate)
VALUES 
('DISC001', 1, 10, '2024-01-01', '2024-12-31'),
('DISC002', 2, 15, '2024-01-01', '2024-12-31'),
('DISC003', 3, 20, '2024-01-01', '2024-12-31'),
('DISC004', 4, 25, '2024-01-01', '2024-12-31'),
('DISC005', 5, 30, '2024-01-01', '2024-12-31');

INSERT INTO enters (CID, discount_code)
VALUES 
(1, 'DISC001'),
(2, 'DISC002'),
(3, 'DISC003'),
(4, 'DISC004'),
(5, 'DISC005');

INSERT INTO updates (OrderID, DID, Ustatus)
VALUES 
('ORD001', 11, true),
('ORD002', 12, true),
('ORD003', 13, false),
('ORD004', 14, true),
('ORD005', 15, false);
