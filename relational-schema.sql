-- SQL Relational Schema

-- User and its IS-A relationships
CREATE TABLE User(
    ID CHAR(10) NOT NULL, 
    firstname CHAR(20),
    lastname CHAR(20), 
    phone_number INT,
    password CHAR(20),
    email CHAR(20),
    PRIMARY KEY(ID)
);

CREATE TABLE Customers(
    ID CHAR(10) NOT NULL,
    address CHAR(20),
    creditcard_no CHAR(20),
    PRIMARY KEY (ID),
    FOREIGN KEY (ID) REFERENCES User
);

CREATE TABLE Admins(
    ID CHAR(10) NOT NULL,
    ssn CHAR(20),
    PRIMARY KEY (ID),
    FOREIGN KEY (ID) REFERENCES User
);

CREATE TABLE Deliverers(
    ID CHAR(10) NOT NULL,
    ssn CHAR(20),
    PRIMARY KEY (ID),
    FOREIGN KEY (ID) REFERENCES User
);

-- Other Attributes

CREATE TABLE Discounts(
    discount_code CHAR(20) NOT NULL,
    discount_perc INT,
    start_date DATE,
    end_date DATE,
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
    name CHAR(20),
    price INT,
    quantity INT,
    type CHAR(20),
    size CHAR(20),
    floral_description CHAR(20),
    PRIMARY KEY (FID)
);


-- Relation Tables

CREATE TABLE enter(
    ID CHAR(10) NOT NULL,
    discount_code CHAR(20) NOT NULL,
    PRIMARY KEY (ID, discount_code),
    FOREIGN KEY (ID) REFERENCES Customers, -- Or User?
    FOREIGN KEY (discount_code) REFERENCES Discounts
);


CREATE TABLE contains(
    OrderID CHAR(10) NOT NULL,
    FID CHAR(10) NOT NULL,
    PRIMARY KEY (OrderID, FID),
    FOREIGN KEY (OrderID) REFERENCES Orders,
    FOREIGN KEY (FID) REFERENCES Flower_arrangement
);


CREATE TABLE deliver(
    OrderID CHAR(10) NOT NULL,
    ID CHAR(10) NOT NULL,
    PRIMARY KEY (OrderID, ID),
    FOREIGN KEY (OrderID) REFERENCES Orders,
    FOREIGN KEY (ID) REFERENCES Deliverers -- Or User?
);

CREATE TABLE place(
    OrderID CHAR(10) NOT NULL,
    ID CHAR(10) NOT NULL,
    PRIMARY KEY (OrderID, ID),
    FOREIGN KEY (OrderID) REFERENCES Orders,
    FOREIGN KEY (ID) REFERENCES Customers -- Or User?
);

CREATE TABLE updates(
    OrderID CHAR(10) NOT NULL,
    ID CHAR(10) NOT NULL,
    PRIMARY KEY (OrderID, ID),
    FOREIGN KEY (OrderID) REFERENCES Orders,
    FOREIGN KEY (ID) REFERENCES Admins -- Or User?
);