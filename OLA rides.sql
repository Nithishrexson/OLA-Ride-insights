CREATE DATABASE ola_project;
USE ola_project;

CREATE TABLE rides (
    Date DATE,
    Time TIME,
    Booking_ID INT PRIMARY KEY AUTO_INCREMENT,
    Booking_Status VARCHAR(50),
    Customer_ID INT,
    Vehicle_Type VARCHAR(50),
    Pickup_Location VARCHAR(100),
    Drop_Location VARCHAR(100),
    V_TAT FLOAT,
    C_TAT FLOAT,
    Canceled_Rides_by_Customer INT,
    Canceled_Rides_by_Driver VARCHAR(100),
    Incomplete_Rides INT,
    Incomplete_Rides_Reason VARCHAR(255),
    Booking_Value DECIMAL(10,2),
    Payment_Method VARCHAR(50),
    Ride_Distance FLOAT,
    Driver_Ratings FLOAT,
    Customer_Rating FLOAT,
    Vehicle_Images VARCHAR(255)
);


LOAD DATA INFILE "N:\OLA_DataSet.csv"
INTO TABLE rides
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

select * from rides;



# 1.Retrieve all successful bookings

SELECT * 
FROM rides
WHERE Booking_Status = 'Success';


# 2.Find the average ride distance for each vehicle type

SELECT Vehicle_Type, ROUND(AVG(Ride_Distance), 2) AS avg_distance
FROM rides
GROUP BY Vehicle_Type;

# 3.Get the total number of cancelled rides by customers

SELECT COUNT(*) AS `cancelled  by customers`
FROM rides
WHERE Canceled_Rides_by_Customer IS NOT NULL;

# 4. List the top 5 customers who booked the highest number of rides

SELECT Customer_ID, COUNT(Booking_ID) AS total_rides
FROM rides
GROUP BY Customer_ID
ORDER BY total_rides DESC
LIMIT 5;

# 5.Get the number of rides cancelled by drivers due to personal and car-related issues

SELECT COUNT(*) AS total_personal_car_issues
FROM rides
WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue';


# 6. Find the maximum and minimum driver ratings for Prime Sedan bookings

SELECT MAX(Driver_Ratings) AS max_rating, MIN(Driver_Ratings) AS min_rating
FROM rides
WHERE Vehicle_Type = 'Prime Sedan';

select * from rides;

# 7. Retrieve all rides where payment was made using UPI

SELECT *
FROM rides
WHERE Payment_Method = 'UPI';

# 8. Find the average customer rating per vehicle type

SELECT Vehicle_Type, ROUND(AVG(Customer_Rating),2) AS avg_customer_rating
FROM rides
GROUP BY Vehicle_Type;

# 9. Calculate the total booking value of rides completed successfully

SELECT SUM(Booking_Value) AS total_booking_value
FROM rides
WHERE Booking_Status = 'Success';

# 10. List all incomplete rides along with the reason:

SELECT Booking_ID, Booking_Status, Incomplete_Rides_Reason
FROM rides
WHERE Incomplete_Rides_Reason IS NOT NULL
  AND Incomplete_Rides_Reason != '';








  
  






