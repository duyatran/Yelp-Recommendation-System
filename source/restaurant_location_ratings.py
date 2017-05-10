import psycopg2
import matplotlib.pyplot as plt
plt.switch_backend('agg')
######### Global variables ###########
NUM_CITIES = 10

# Find the NUM_CITIES cities with the largest number of businesses (sum of check ins from all restaurants in town)
get_cities_cm = "with city_bus_count AS \
(SELECT city, count(*) as bus_count \
FROM businesses \
GROUP BY city) \
SELECT city \
FROM city_bus_count \
ORDER BY bus_count DESC \
limit " + str(NUM_CITIES) + ";"
try:
    conn = psycopg2.connect("dbname=yelp user=vagrant")
except:
    print "Could not connect to the database yelp"
cur_city = conn.cursor()

out_dir = "../output/restaurants_location_ratings/"
light_color = "#DDD8D8"
dark_color = "#0D1FD2"

#######################################

######### CODE ################
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
    """
    :param cur: the cursor that executes psql comands
    :return: list of raw citi names and list of cities name in computer scientist- friendly format
    """
    raw_cities = [] # list of city names as it appears in the data base
    cities_time_fnames = [] # list of file names for each city. Each file is in the form cityName_check_ins.txt
    for record in cur:
        raw_cities.append(record[0])
        cities_time_fnames.append(process_city_fname(record[0]))
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
        cities_time_fnames.append(process_city_fname(record[0]))
    return raw_cities, cities_time_fnames

####### Get 10 cities with the most number of check-ins, and the corresponding computer-scientist-friendly file names of such cities
####### These variables are used often, so we want to declare them as global variables
raw_cities, cities_fnames = get_cities()
#cities_time_fnames = ['LasVegas', 'Phoenix', 'Scottsdale', 'Toronto', 'Charlotte', 'Henderson', 'Tempe', 'Pittsburgh',"Montr\xc3\xa9Al", 'Mesa']

def write_restaurant_by_city_record(city, city_fname, cur):
    out_fname = out_dir + city_fname + "_res_loc_ratings.txt"
    f = open(out_fname, 'w')
    for record in cur:
        f.write(",".join([str(entry) for entry in record]))
        f.write("\n")
    f.close()

def create_res_loc_ratings_by_city():
    for i, city in enumerate(raw_cities):
        command = "SELECT bus_id, bus_name , latitude, longitude , stars \
                  FROM businesses \
                  WHERE city = \'" + city + "\';"
        try:
            cur_city.execute(command)
        except:
            print "There were problems executing the command " + command
        write_restaurant_by_city_record(city, cities_fnames[i], cur_city)

#create_res_loc_ratings_by_city()

def calculate_city_stars(city_fname):
    """

    :param city_fname: Given the name of a file in
    :return:
    """
    city_res_loc_stars_fname = out_dir + city_fname + "_res_loc_ratings.txt"
    f = open(city_res_loc_stars_fname, 'r')
    stars = 0
    num_res = 0
    for line in f:
        stars += float((line.split(","))[-1])
        num_res += 1
    f.close()
    return float(stars) / float(num_res)

def draw_restaurants_loc_ratings_by_city(city_fname, avg_star):
    #open file to read data of restaurants locations and stars
    city_res_loc_stars_fname = out_dir + city_fname + "_res_loc_ratings.txt"
    f = open(city_res_loc_stars_fname, 'r')
    # name of file to store the figure we are trying to plot
    save_fname = out_dir + city_fname + "_res_loc_ratings.png"

    # open figure
    fig = plt.figure(figsize=(8,6), dpi = 300)
    ax = fig.add_subplot(111)
    # declare lists of x-coordinates and y-coordinates for the dark dots (above_average stars) and the light dots (below_average stars)
    above_avg_x = [] # latitude
    above_avg_y = [] # longitude
    below_avg_x = []
    below_avg_y = []
    # for each restaurant in town
    for line in f:
        star = float((line.split(","))[-1])
        lat = float((line.split(","))[-3])
        long = float((line.split(","))[-2])
        if star >= avg_star:
            above_avg_x.append(lat)
            above_avg_y.append(long)
        else:
            below_avg_x.append(lat)
            below_avg_y.append(long)
    # close text file
    f.close()
    # draw scatter
    ax.scatter(above_avg_x, above_avg_y, color = dark_color, alpha = 0.5)
    ax.scatter(below_avg_x, below_avg_y, color = light_color, alpha = 0.025)

    # save figure
    fig.subplots_adjust(left = 0.05, bottom = 0.05, right = 0.95, top = 0.95)
    fig.savefig(save_fname, format='png', dpi = 300)

def plot_res_loc_ratings_by_city(raw_cities, cities_fnames):
    """
    raw_cities: list of raw name of cities as it appears in database
    cities_fnames: list of name of cities as it should appear in any output file name
    :return: Generate plots of restaurants location and high/low ratings in  a city
    """
    # Here we just generate analysis for the most frequently checked in cities
    for city in cities_fnames:
        avg_star = calculate_city_stars(city)
        draw_restaurants_loc_ratings_by_city(city, avg_star)
#plot_res_loc_ratings_by_city()