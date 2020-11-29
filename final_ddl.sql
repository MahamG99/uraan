



CREATE TABLE `Bank` (
  `Account_Number` varchar(20) NOT NULL,
  `Bank_Name` varchar(20) NOT NULL,
  `Security_Key` int NOT NULL,
  `Expiry_Date` date DEFAULT NULL,
  `Card_Type` varchar(15) NOT NULL,
  `Account_Balance` int NOT NULL,
  PRIMARY KEY (`Account_Number`)
)

CREATE TABLE `Airline` (
  `Airline_Name` varchar(30) NOT NULL,
  `Account_Number` varchar(20) NOT NULL,
  PRIMARY KEY (`Airline_Name`),
  KEY `Airline_fk0` (`Account_Number`),
  CONSTRAINT `Airline_fk0` FOREIGN KEY (`Account_Number`) REFERENCES `Bank` (`Account_Number`) ON DELETE CASCADE
)

CREATE TABLE `Agents` (
  `Agent_id` int NOT NULL AUTO_INCREMENT,
  `First_Name` varchar(20) NOT NULL,
  `Last_Name` varchar(20) NOT NULL,
  `Airline_Name` varchar(30) NOT NULL,
  `Email` varchar(30) NOT NULL,
  `Password` varchar(10) NOT NULL,
  PRIMARY KEY (`Agent_id`),
  KEY `Agents_fk0` (`Airline_Name`),
  CONSTRAINT `Agents_fk0` FOREIGN KEY (`Airline_Name`) REFERENCES `Airline` (`Airline_Name`) ON DELETE CASCADE
)

CREATE TABLE `Bookings` (
  `Booking_ID` int NOT NULL,
  `Flight_Number` varchar(10) NOT NULL,
  `Passenger_Name` varchar(40) NOT NULL,
  `Customer_ID` int NOT NULL,
  `Number_of_Connections` int NOT NULL,
  `Price` int DEFAULT NULL,
  `Seat_number` varchar(5) NOT NULL,
  `Checkin_status` tinyint(1) NOT NULL,
  `Travel_class` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`Booking_ID`,`Flight_Number`,`Passenger_Name`),
  KEY `Bookings_fk0` (`Flight_Number`),
  KEY `Bookings_fk1` (`Customer_ID`),
  KEY `Bookings_fk2` (`Seat_number`),
  CONSTRAINT `Bookings_fk0` FOREIGN KEY (`Flight_Number`) REFERENCES `Flights` (`Flight_Number`) ON DELETE CASCADE,
  CONSTRAINT `Bookings_fk1` FOREIGN KEY (`Customer_ID`) REFERENCES `Customers` (`Customer_ID`) ON DELETE CASCADE,
  CONSTRAINT `Bookings_fk2` FOREIGN KEY (`Seat_number`) REFERENCES `Seat` (`Seat_Number`),
  CONSTRAINT `bookings_chk_1` CHECK ((`Travel_class` in (_utf8mb4'Economy',_utf8mb4'Business',_utf8mb4'First'))),
  CONSTRAINT `bookings_chk_2` CHECK ((`Price` > 0))
)

CREATE TABLE `customers` (
  `Customer_ID` int NOT NULL AUTO_INCREMENT,
  `Password` char(8) NOT NULL,
  `First_Name` varchar(20) NOT NULL,
  `Last_Name` varchar(20) NOT NULL,
  `Email` varchar(30) NOT NULL,
  `Passport_Number` char(9) DEFAULT NULL,
  `Phone_Number` varchar(20) DEFAULT NULL,
  `Nationality` varchar(60) DEFAULT NULL,
  `Age` int DEFAULT NULL,
  `Gender` varchar(8) DEFAULT NULL,
  `Flyer_Points` int DEFAULT NULL,
  `Account_Number` varchar(20) DEFAULT NULL,
  `Discount` int DEFAULT NULL,
  PRIMARY KEY (`Customer_ID`),
  KEY `Customers_fk0` (`Account_Number`),
  CONSTRAINT `Customers_fk0` FOREIGN KEY (`Account_Number`) REFERENCES `Bank` (`Account_Number`),
  CONSTRAINT `customers_chk_1` CHECK ((`Gender` in (_utf8mb4'Male',_utf8mb4'Female',_utf8mb4'Other')))
)

CREATE TABLE `Family` (
  `Customer_ID` int NOT NULL,
  `First_Name` varchar(20) NOT NULL,
  `Last_Name` varchar(20) NOT NULL,
  `Passport_Number` char(9) NOT NULL,
  `Phone_number` int NOT NULL,
  `Nationality` varchar(60) NOT NULL,
  `Age` int NOT NULL,
  `Gender` varchar(8) DEFAULT NULL,
  `Relationship` varchar(15) NOT NULL,
  PRIMARY KEY (`Customer_ID`,`First_Name`,`Last_Name`),
  CONSTRAINT `Family_fk0` FOREIGN KEY (`Customer_ID`) REFERENCES `Customers` (`Customer_ID`) ON DELETE CASCADE,
  CONSTRAINT `family_chk_1` CHECK ((`Gender` in (_utf8mb4'Male',_utf8mb4'Female',_utf8mb4'Other')))
)

CREATE TABLE `Flight Price` (
  `Flight_Number` varchar(10) NOT NULL,
  `Travel_class` varchar(15) NOT NULL,
  `Passenger_type` varchar(10) NOT NULL,
  `Price` int NOT NULL,
  PRIMARY KEY (`Flight_Number`,`Travel_class`,`Passenger_type`),
  CONSTRAINT `Flight Price_fk0` FOREIGN KEY (`Flight_Number`) REFERENCES `Flights` (`Flight_Number`)
)

CREATE TABLE `Flights` (
  `Flight_Number` varchar(10) NOT NULL,
  `Departure` char(3) NOT NULL,
  `Arrival` char(3) NOT NULL,
  `Departure_Time` datetime NOT NULL,
  `Arrival_Time` datetime NOT NULL,
  `Airline_Name` varchar(30) NOT NULL,
  `Plane_type` varchar(20) NOT NULL,
  `Status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`Flight_Number`),
  KEY `Flights_fk0` (`Airline_Name`),
  CONSTRAINT `Flights_fk0` FOREIGN KEY (`Airline_Name`) REFERENCES `Airline` (`Airline_Name`) ON DELETE CASCADE,
  CONSTRAINT `flights_chk_1` CHECK ((`Status` in (_utf8mb4'On-time',_utf8mb4'Delayed',_utf8mb4'Cancelled')))
)

CREATE TABLE `Seat` (
  `Seat_Number` char(4) NOT NULL,
  `Type` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`Seat_Number`),
  CONSTRAINT `seat_chk_1` CHECK ((`Type` in (_utf8mb4'Aisle',_utf8mb4'Window',_utf8mb4'Bassinet',_utf8mb4'Middle',_utf8mb4'Emergency')))
)