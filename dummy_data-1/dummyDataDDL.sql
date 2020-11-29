CREATE TABLE `Bank` (
  `Account_Number` varchar(20) NOT NULL,
  `Bank_Name` varchar(20) NOT NULL,
  `Security_Key` int NOT NULL,
  `Expiry_Date` date DEFAULT NULL,
  `Card_Type` varchar(15) NOT NULL,
  `Account_Balance` int NOT NULL,
  PRIMARY KEY (`Account_Number`)
);

CREATE TABLE `Airline` (
  `Airline_Name` varchar(30) NOT NULL,
  `Account_Number` varchar(20) NOT NULL,
  PRIMARY KEY (`Airline_Name`),
  KEY `Airline_fk0` (`Account_Number`),
  CONSTRAINT `Airline_fk0` FOREIGN KEY (`Account_Number`) REFERENCES `Bank` (`Account_Number`) ON DELETE CASCADE
);

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
);

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
);
