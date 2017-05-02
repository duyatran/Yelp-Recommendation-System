import psycopg2
import matplotlib.pyplot as plt
plt.switch_backend('agg')
######### Global variables ###########
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

out_dir = "../output/check_in_time_by_cities/"
day_per_week = 7
hour_per_day = 24
day_colors = ['#F93307', '#F9BB07', '#54F907', '#07F9F2', '#0719F9', '#F907EE', '#F90728']

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
raw_cities, cities_time_fnames = get_cities()
#cities_time_fnames = ['LasVegas', 'Phoenix', 'Scottsdale', 'Toronto', 'Charlotte', 'Henderson', 'Tempe', 'Pittsburgh',"Chandler", 'Mesa']
def write_city_check_ins(record, num_res, f):
    # write day and time first
    for i in range(len(record) - 1):
        f.write(str(record[i]) + ",")
    # write the average check in per restaurant
    avg_check_ins = float(record[-1]) / float(num_res)
    f.write(str(avg_check_ins) + "\n")


def create_popular_time_cities():
    """
    :return: (1)Find cities with the most number of check ins
             (2) For each city, create a file that records the day, hour, count of check-ins
             this results is accumulative for each city (for each city, count of check-ins is the sum of check-ins in all restaurants in town
             at each day-hour combination)
    """
    # For each city that we wish to consider (cities that have the most number of check-ins)
    for i, city in enumerate(raw_cities):
        city_fname = out_dir + cities_time_fnames[i] + "_check_ins.txt"
        fout = open(city_fname, 'w')
        # find the number of restaurants in this city
        numRestaurantsCommand = "SELECT count(*) \
                                FROM businesses \
                                WHERE city = \'" + city + "\'"
        try:
            cur_city.execute(numRestaurantsCommand)
        except:
            print "There were problems executing the command " + numRestaurantsCommand
        num_res = 0
        for record in cur_city:
            num_res = record[0]
        # command to get the counts of check-ins in each time frame
        command = "WITH city_business AS \
                  (select distinct city, bus_name, day, hour, COUNT \
                  FROM businesses, check_ins \
                  WHERE businesses.bus_id = check_ins.bus_id \
                  AND city = \'"+ city + "\') \
                  SELECT DISTINCT day, hour, sum(count)  as check_ins \
                  FROM city_business \
                  GROUP BY day, hour;"
        #execute the command
        try:
            cur_city.execute(command)
        except:
            print "There were problems executing the command " + command
        #write the data out
        for record in cur_city:
            write_city_check_ins(record, num_res, fout)
        fout.close()

def determineTickInterval(r,l): # determine tick interval given a range (r)
	# r: range
	# l: limit (increase l for more ticks)
	candidates = [1,2,5,10,20,30,50,100]
	for candidate in candidates:
		if r/candidate<l:
			return candidate
	return 1

def plot_popular_time_one_city(city_fname):
    save_fname = out_dir + city_fname + "_check_ins.png"
    check_in_dict = {} # a dictionary with keys are the time-slots in the day and values are the average number of check-ins per restaurant
    # put in default value : 0 check-ins
    for day in range(day_per_week):
        for hour in range(hour_per_day):
            check_in_dict[(day, hour)] = 0
    # process data from the check_ins.txt files
    input_fname = out_dir + city_fname + "_check_ins.txt"
    f = open(input_fname, 'r')
    for line in f:
        d_h_ci = line.split(",")
        (day, hour) = (int(d_h_ci[0]), int(d_h_ci[1]))
        check_in_dict[(day, hour)] = float(d_h_ci[2])
    # Put all data of check_in frequencies into list
    freq_list = []
    for day in range(day_per_week):
        for hour in range(hour_per_day):
            freq_list.append(check_in_dict[(day, hour)])
    fig = plt.figure(figsize=(5,3), dpi = 300)
    ax = fig.add_subplot(111)
    for day in range(day_per_week):
        ax.bar(range(day * hour_per_day, (day + 1) * hour_per_day), freq_list[day * hour_per_day:(day + 1) * hour_per_day],\
               color = day_colors[day], linewidth = 0.01)
    #plt.show()
    fig.subplots_adjust(left = 0.05, bottom = 0.05, right = 0.95, top = 0.95)
    fig.savefig(save_fname, format='png', dpi = 300)

def plot_popular_time_all_cities():
    for city in cities_time_fnames:
        plot_popular_time_one_city(city)

