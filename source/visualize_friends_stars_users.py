import psycopg2
import matplotlib.pyplot as plt
plt.switch_backend('agg')

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
        exit(0, "PSQL Execution problem")
    print "After executing the command to find users' number of friends and ratings"
    num_friends = []
    ratings = []
    for record in cur:
        num_friends.append(record[0])
        ratings.append(record[1])
    print "After obtaining data of users' number of friends and ratings"
    plt.figure(figsize=(8, 6))
    plt.plot(num_friends, ratings, 'o', alpha = 0.1)
    print "After plotting"
    plt.ylabel("Ratings")
    plt.xlabel("Number of friends")
    plt.title("Distributions of users' number of friends and ratings")
    print "After notating"
    plt.show()
    print "Done ..."


