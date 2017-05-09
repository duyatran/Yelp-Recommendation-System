import psycopg2
#plt.switch_backend('agg')

out_dir = "../output/ratings_distribution"
try:
    conn = psycopg2.connect("dbname=yelp user=vagrant")
except:
    print "Could not connect to the database yelp"
    exit(1, "Could not connect to the database")
cur = conn.cursor()

def get_star_distribution():
    command = "SELECT stars, count(*) \
              FROM reviews \
              GROUP by stars;"
    try:
        cur.execute(command)
    except:
        print "There were problems executing the command " + command
        exit(0, "PSQL Execution problem")
    print "Done executing the command to find users' number of friends and ratings"
    stars = []
    num_stars = []
    for record in cur:
        stars.append(record[0])
        num_stars.append(record[1])
    return stars, num_stars

