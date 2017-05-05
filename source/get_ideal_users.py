import psycopg2
import macros as m
# get_user_id_command is psql command used to get users id that have more than 1000 reivew on yelp

try:
    conn = psycopg2.connect("dbname=yelp user=vagrant")
except:
    print "Could not connect to the database yelp"
cur = conn.cursor()

def get_more_1000_users():
    get_user_more_1000_command = "with user_review_cnt as \
    (select user_id , count(*) as review_count \
    FROM reviews \
    GROUP BY user_id) \
    SELECT user_id \
    FROM user_review_cnt \
    WHERE review_count >= 1000;"

    try:
        cur.execute(get_user_more_1000_command)
    except:
        print "There were problems executing the command " + get_user_more_1000_command
    f = open(m.user_more_1000_fname, 'w')
    for record in cur:
        f.write(record[0] + "\n")
    f.close()

def get_users_limit(num_users, fname):
    """
    :param num_users: Number of users that we want to run recommendations on.
    This function will choose the num_users users with the most number of reviews
    :fname: name of the file to store the output
    :return: Write into a file that has the id of users that we want to
    """
    get_users_limit_command = "with user_review_cnt as \
    (select user_id , count(*) as review_count \
    FROM reviews \
    GROUP BY user_id) \
    SELECT user_id \
    FROM user_review_cnt \
    ORDER BY review_count DESC \
    limit " + str(num_users) + " ;"
    try:
        cur.execute(get_users_limit_command)
    except:
        print "There were problems executing the command " + get_users_limit_command
    f = open (fname, 'w')
    for record in cur:
        f.write(record[0] + "\n")
    f.close()