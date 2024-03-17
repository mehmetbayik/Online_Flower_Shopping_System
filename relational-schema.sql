-- SQL Relational Schema

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

CREATE TABLE Customers(
    CID CHAR(10) NOT NULL,
    Caddress CHAR(20),
    creditcard_no CHAR(20),
    PRIMARY KEY (CID),
    FOREIGN KEY (CID) REFERENCES User(ID)
);

CREATE TABLE Admins(
    AID CHAR(10) NOT NULL,
    ssn CHAR(20),
    PRIMARY KEY (AID),
    FOREIGN KEY (AID) REFERENCES User(ID)
);

CREATE TABLE Deliverers(
    DID CHAR(10) NOT NULL,
    ssn CHAR(20),
    PRIMARY KEY (DID),
    FOREIGN KEY (DID) REFERENCES User(ID)
);

-- Other Attributes

CREATE TABLE Discounts(
    discount_code CHAR(20) NOT NULL,
    discount_perc INT,
    Sdate DATE,
    Edate DATE,
    PRIMARY KEY (discount_code)
);

CREATE TABLE Orders(
    OrderID CHAR(10) NOT NULL,
    order_date DATE,
    delivery_date DATE,
    paid_price INT,
    gift_note CHAR(20),
    PRIMARY KEY (OrderID)
);

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

CREATE TABLE enter(
    CID CHAR(10) NOT NULL,
    discount_code CHAR(20) NOT NULL,
    PRIMARY KEY (discount_code),
    FOREIGN KEY (CID) REFERENCES Customers(CID),
    FOREIGN KEY (discount_code) REFERENCES Discounts(discount_code)
);


CREATE TABLE contains(
    OrderID CHAR(10) NOT NULL,
    FID CHAR(10) NOT NULL,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (FID) REFERENCES Flower_arrangement(FID)
);


CREATE TABLE deliver(
    OrderID CHAR(10) NOT NULL,
    DID CHAR(10) NOT NULL,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (DID) REFERENCES Deliverers(DID) -- Or User?
);

CREATE TABLE place(
    OrderID CHAR(10) NOT NULL,
    CID CHAR(10) NOT NULL,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (CID) REFERENCES Customers(CID) -- Or User?
);

CREATE TABLE updates(
    OrderID CHAR(10) NOT NULL,
    DID CHAR(10) NOT NULL,
    Ustatus BOOLEAN,
    PRIMARY KEY (OrderID, DID),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (DID) REFERENCES Deliverers(DID) -- Or User?
);