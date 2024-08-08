-- This script creates a MySQL function called SafeDiv that performs division between two integers.
-- If the second integer is zero, it returns 0 to handle division by zero errors. Otherwise, it returns the result of the division.
DELIMITER //

CREATE FUNCTION SafeDiv(a INT, b INT) RETURNS FLOAT
BEGIN
    IF b = 0 THEN
        RETURN 0;
    ELSE
        RETURN a / b;
    END IF;
END //

DELIMITER ;

