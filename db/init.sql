CREATE TABLE parking_spots 
(
    spot_number INT PRIMARY KEY,
    floor INT NOT NULL,
    occupied VARCHAR(3) NOT NULL CHECK (occupied IN ('Да', 'Нет')),
    car_plate VARCHAR(20)
);

INSERT INTO parking_spots (spot_number, floor, occupied, car_plate) VALUES
(1, 1, 'Да', 'мо550с77'),
(2, 1, 'Да', 'е777кх97'),
(3, 1, 'Нет', NULL),
(4, 2, 'Да', 'а797еа799'),
(5, 2, 'Нет', NULL);

