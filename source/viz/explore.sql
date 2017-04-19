-- select avg(array_length(attributes, 1)) from businesses;
--  avg
-- --------------------
--  8.9244742926345921

-- select max(array_length(categories, 1)) from businesses;
--  avg
-- -----
--  3.6703652945800608
-- (1 row)

-- select avg(review_count) from users;
--  avg
-- ---------------------
--  24.3193324085515119

-- From the two queries above, the size of list of attributes for each user's model would not be too big (about 9+4 = 13)

--select count(*) from users where review_count>1000;
--  count
-- -------
--   1019
