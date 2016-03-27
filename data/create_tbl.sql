# Create table restaurants
CREATE TABLE restaurants (
id SERIAL PRIMARY KEY,
rest_id BIGINT,
city TEXT,
rest_name TEXT,
menu_item TEXT,
menu_section TEXT,
count INT);

# Sample insert 1
INSERT INTO restaurants (id, rest_id, city, rest_name, menu_item, menu_section, count) 
VALUES (1, 120, 'Villanueva', 'Chicken', NULL, 5);

# Sample insert 2
INSERT INTO restaurants (id, rest_id, rest_name, menu_item, menu_section, count)
VALUES(36, 320, 'Marlowe''s', 'Tacos', NULL, 36);