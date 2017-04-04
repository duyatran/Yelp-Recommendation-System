import psycopg2

NUM_CITIES = 10

# Find the NUM_CITIES cities with the largest number of check-ins (sum of check ins from all restaurants in town)
get_cities_cm = "WITH city_business AS \
(select distinct city, bus_name, day, hour, COUNT \
FROM businesses, check_ins \
WHERE businesses.bus_id = check_ins.bus_id) \
SELECT DISTINCT city, sum(count) as check_ins \
from city_business \
GROUP BY city \
ORDER BY check_ins DESC \
limit " + str(NUM_CITIES) + ";"
try:
    conn = psycopg2.connect("dbname=yelp user=vagrant")
except:
    print "Could not connect to the database yelp"
cur_city = conn.cursor()
cur_check_in = conn.cursor()

def process_city_fname(raw):
    """
    :param raw: city names as appear in the database
    :return: city names in format: NewYork, LosAngeles, etc.
    """
    result = ""
    words = raw.split()
    for word in words:
        result += word.title()
    return result

def create_city_fnames(cur):
    raw_cities = [] # list of city names as it appears in the data base
    cities_time_fnames = [] # list of file names for each city. Each file is in the form cityName_check_ins.txt
    for record in cur:
        raw_cities.append(record[0])
        cities_time_fnames.append(process_city_fname(record[0]) + "_check_ins.txt")
    return raw_cities, cities_time_fnames

def get_cities():
    """
    :return: Get (1) the list of cities names (raw: city names as appear in the database)
                 (2) the list of cities files names (in format: NewYork_check_ins.txt, LosAngeles_check_ins.txt, etc.)
            with only NUM_CITIES that  have the most accumulative number of check-ins
    """
    try:
        cur_city.execute(get_cities_cm)
    except:
        print "There were problems executing the command " + get_cities_cm
    raw_cities = [] # list of city names as it appears in the data base
    cities_time_fnames = [] # list of file names for each city. Each file is in the form cityName_check_ins.txt
    for record in cur_city:
        raw_cities.append(record[0])
        cities_time_fnames.append("../output/" + process_city_fname(record[0]) + "_check_ins.txt")
    return raw_cities, cities_time_fnames

def write_city_check_ins(record, f):
    for i in range(len(record) - 1):
        f.write(str(record[i]) + ",")
    f.write(str(record[-1]) + "\n")

def create_popular_time_cities():
    """
    :return: (1)Find cities with the most number of check ins
             (2) For each city, create a file that records the day, hour, count of check-ins
             this results is accumulative for each city (for each city, count of check-ins is the sum of check-ins in all restaurants in town
             at each day-hour combination)
    """
    # Find cities with the most number of check ins
    raw_cities, cities_time_fnames = get_cities()
    for i, city in enumerate(raw_cities):
        fout = open(cities_time_fnames[i], 'w')
        # command to get the counts of check-ins in each time frame
        command = "WITH city_business AS \
                  (select distinct city, bus_name, day, hour, COUNT \
                  FROM businesses, check_ins \
                  WHERE businesses.bus_id = check_ins.bus_id \
                  AND city = \'"+ city + "\') \
                  SELECT DISTINCT day, hour, sum(count) as check_ins \
                  FROM city_business \
                  GROUP BY day, hour;"
        #execute the command
        try:
            cur_city.execute(command)
        except:
            print "There were problems executing the command " + command
        #write the data out
        for record in cur_city:
            write_city_check_ins(record, fout)
        fout.close()
create_popular_time_cities()
