CREATE TABLE `Agents` (
  `Agent_id` int NOT NULL AUTO_INCREMENT,
  `First_Name` varchar(20) NOT NULL,
  `Last_Name` varchar(20) NOT NULL,
  `Airline_Name` varchar(30) NOT NULL,
  `Email` varchar(30) NOT NULL,
  `Password` varchar(10) NOT NULL,
  PRIMARY KEY (`Agent_id`),
  KEY `Agents_fk0` (`Airline_Name`)
  
)
CREATE TABLE `customers` (
  `Customer_ID` int NOT NULL AUTO_INCREMENT,
  `Password` char(8) NOT NULL,
  `First_Name` varchar(20) NOT NULL,
  `Last_Name` varchar(20) NOT NULL,
  `Email` varchar(30) NOT NULL,
  `Passport_Number` char(9) DEFAULT NULL,
  `Phone_Number` int DEFAULT NULL,
  `Nationality` varchar(60) DEFAULT NULL,
  `Age` int DEFAULT NULL,
  `Gender` varchar(8) DEFAULT NULL,
  `Flyer_Points` int DEFAULT NULL,
  `Account_Number` varchar(20) DEFAULT NULL,
  `Discount` int DEFAULT NULL,
  PRIMARY KEY (`Customer_ID`),
  CHECK (`Gender` in ('Male', 'Female', 'Other'))
) 

