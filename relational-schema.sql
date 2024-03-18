-- SQL Relational Schema
-- Example Syntax:



-- User and its IS-A relationships
CREATE TABLE User(
   ID CHAR(10) NOT NULL,
   firstname CHAR(20),
   lastname CHAR(20),
   phone_number INT,
   Upassword CHAR(20),
   email CHAR(20),
   PRIMARY KEY(ID)
);


User {
	ID-Numeric-Not Null
	firstname-Text
	lastname-Text
	phone_number-Numeric
	Upassword-Text
	email-Text
	Primary Key (ID)
}


CREATE TABLE Customer(
   CID CHAR(10) NOT NULL,
   Caddress CHAR(20),
   creditcard_no CHAR(20),
   PRIMARY KEY (CID),
   FOREIGN KEY (CID) REFERENCES User(ID)
);


Customer {
	CID-Numeric-Not Null
	Caddress-Text
	creditcard_no-Numeric
	Primary Key (CID)
	Foreign Key (CID) -> User (ID)
}


CREATE TABLE Admin(
   AID CHAR(10) NOT NULL,
   ssn CHAR(20),
   PRIMARY KEY (AID),
   FOREIGN KEY (AID) REFERENCES User(ID)
);


Admin {
	AID-Numeric-Not Null
	ssn-Numeric
	Primary Key (AID)
	Foreign Key (AID) -> User (ID)
}


CREATE TABLE Deliverer(
   DID CHAR(10) NOT NULL,
   ssn CHAR(20),
   PRIMARY KEY (DID),
   FOREIGN KEY (DID) REFERENCES User(ID)
);


Deliverer {
	DID-Numeric-Not Null
	ssn-Numeric
	Primary Key (DID)
	Foreign Key (DID) -> User (ID)
}
	
-- Other Attributes


CREATE TABLE Discount(
   discount_code CHAR(20) NOT NULL,
   discount_perc INT,
   Sdate DATE,
   Edate DATE,
   PRIMARY KEY (discount_code)
);


Discount {
	discount_code-Text-Not Null
discount_perc -Numeric
	Sdate -Date
Edate -Date
	Primary Key (discount_code)
	}


CREATE TABLE Orders(
   OrderID CHAR(10) NOT NULL,
   order_date DATE,
   delivery_date DATE,
   paid_price INT,
   gift_note CHAR(20),
   PRIMARY KEY (OrderID)
);
Orders{
OrderID -Text-Not Null
	order_date -Date
delivery_date -Date
	paid_price -Numeric
gift_note -Text
	Primary Key (OrderID )
	}




CREATE TABLE Flower_arrangement(
   FID CHAR(10) NOT NULL,
   Fname CHAR(20),
   price INT,
   quantity INT,
   Ftype CHAR(20),
   Fsize CHAR(20),
   floral_description CHAR(20),
   PRIMARY KEY (FID)
);




-- Relation Tables


CREATE TABLE enters(
   CID CHAR(10) NOT NULL,
   discount_code CHAR(20) NOT NULL,
   PRIMARY KEY (discount_code),
   FOREIGN KEY (CID) REFERENCES Customer(CID),
   FOREIGN KEY (discount_code) REFERENCES Discount(discount_code)
);




CREATE TABLE contains(
   OrderID CHAR(10) NOT NULL,
   FID CHAR(10) NOT NULL,
   PRIMARY KEY (OrderID),
   FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
   FOREIGN KEY (FID) REFERENCES Flower_arrangement(FID)
);




CREATE TABLE delivers(
   OrderID CHAR(10) NOT NULL,
   DID CHAR(10) NOT NULL,
   PRIMARY KEY (OrderID),
   FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
   FOREIGN KEY (DID) REFERENCES Deliverer(DID) -- Or User?
);


CREATE TABLE places(
   OrderID CHAR(10) NOT NULL,
   CID CHAR(10) NOT NULL,
   PRIMARY KEY (OrderID),
   FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
   FOREIGN KEY (CID) REFERENCES Customer(CID) -- Or User?
);


CREATE TABLE updates(
   OrderID CHAR(10) NOT NULL,
   DID CHAR(10) NOT NULL,
   Ustatus BOOLEAN,
   PRIMARY KEY (OrderID, DID),
   FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
   FOREIGN KEY (DID) REFERENCES Deliverer(DID) -- Or User?
);

