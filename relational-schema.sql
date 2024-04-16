-- SQL Relational Schema

-- User and its IS-A relationships
CREATE TABLE User(
   ID INT NOT NULL UNIQUE,
   firstname CHAR(20),
   lastname CHAR(20),
   phone_number INT,
   Upassword CHAR(20) UNIQUE,
   email CHAR(20) UNIQUE,
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
   Containing_ID INT NOT NULL,
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
   CID INT NOT NULL UNIQUE,
   discount_code CHAR(20) NOT NULL UNIQUE,
   PRIMARY KEY (discount_code),
   FOREIGN KEY (CID) REFERENCES Customer(CID),
   FOREIGN KEY (discount_code) REFERENCES Discount(discount_code)
);

CREATE TABLE updates(
   OrderID CHAR(10) NOT NULL UNIQUE,
   DID CHAR(10) NOT NULL UNIQUE,
   Ustatus BOOLEAN,
   PRIMARY KEY (OrderID, DID),
   FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
   FOREIGN KEY (DID) REFERENCES Deliverer(DID)
);

