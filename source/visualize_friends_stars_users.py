import psycopg2
import matplotlib.pyplot as plt
#plt.switch_backend('agg')

out_dir = "../output/friends_ratings_users"
try:
    conn = psycopg2.connect("dbname=yelp user=vagrant")
except:
    print "Could not connect to the database yelp"
    exit(1, "Could not connect to the database")
cur = conn.cursor()

def get_friends_ratings_friends():
    command = "Select array_length(friends, 1) as num_friends, avg_stars \
    from users;"
    try:
        cur.execute(command)
    except:
        print "There were problems executing the command " + command
    print "Done executing the command to find users' number of friends and ratings"
    num_friends = []
    ratings = []
    for record in cur:
        num_friends.append(record[0])
        ratings.append(record[1])
    return num_friends, ratings

