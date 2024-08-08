-- Query to count names starting with 'a'
CREATE INDEX idx_name_first
ON names(name(1));
