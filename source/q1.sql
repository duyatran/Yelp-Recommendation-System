WITH city_business AS
(select distinct city, bus_name, day, hour, COUNT
FROM businesses, check_ins
WHERE businesses.bus_id = check_ins.bus_id
AND city = 'Las Vegas')
SELECT DISTINCT day, hour, sum(count) as check_ins
FROM city_business
GROUP BY day, hour;