import psycopg2
# get_user_id_command is psql command used to get users id that have more than 1000 reivew on yelp
get_user_id_command = "with user_review_cnt as \
(select user_id , count(*) as review_count \
FROM reviews \
GROUP BY user_id) \
SELECT user_id \
FROM user_review_cnt \
WHERE review_count >= 1000;"

ideal_user_save_file = "../output/ideal_users.txt"
try:
    conn = psycopg2.connect("dbname=yelp user=vagrant")
except:
    print "Could not connect to the database yelp"
cur = conn.cursor()

def get_ideal_users():
    try:
        cur.execute(get_user_id_command)
    except:
        print "There were problems executing the command " + get_user_id_command
    f = open(ideal_user_save_file, 'w')
    for record in cur:
        f.write(record[0] + "\n")
    f.close()

get_ideal_users()