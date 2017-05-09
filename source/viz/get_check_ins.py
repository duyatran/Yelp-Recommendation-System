import psycopg2

NUM_CITIES = 10
### get the 10000 bus_id, num_check_ins that have the highgest num check ins
get_highest_check_ins = "SELECT bus_id, count(*) as num_check_ins\
                        FROM check_ins \
                        GROUP BY bus_id \
                        ORDER BY num_check_ins \
                        DESC \
                        limit" + str(NUM_CITIES) + " ;"
try:
    conn = psycopg2.connect("dbname=yelp user=vagrant")
except:
    print "Could not connect to the database yelp"
cur = conn.cursor()

def querry_and_record(fout_name, command):
    fout = open(fout_name, 'w')
    try:
        cur.execute(command)
    except:
        print "There were problems executing the command " + command
    for record in cur:
        for i in range(len(record) - 1):
            fout.write(str(record[i]) + ",")
        fout.write(str(record[-1]) + "\n")
    fout.close()

querry_and_record('../output/highest_check_in.txt', get_highest_check_ins)