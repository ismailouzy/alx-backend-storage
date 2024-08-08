-- This script creates a view called need_meeting that lists students
-- who have a score less than 80 and either have no last meeting date
-- or have a last meeting date older than one month from today.

-- Create the need_meeting view
CREATE VIEW need_meeting AS
SELECT name
FROM students
WHERE score < 80
AND (last_meeting IS NULL OR last_meeting < CURDATE() - INTERVAL 1 MONTH);

