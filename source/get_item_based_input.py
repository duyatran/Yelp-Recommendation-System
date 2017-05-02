import psycopg2
from collections import Counter
# get_user_id_command is psql command used to get users id that have more than 1000 reivew on yelp
item_based_command = "Select user_id, bus_id, stars \
                      from reviews;"

item_based_fname = "../output/item_based_input.txt"
try:
    conn = psycopg2.connect("dbname=yelp user=vagrant")
except:
    print "Could not connect to the database yelp"
cur = conn.cursor()

def get_item_based_input_all():
    try:
        cur.execute(item_based_command)
    except:
        print "There were problems executing the command " + item_based_command
        exit(1, "Could not execute psql command")
    f = open(item_based_fname, 'w')
    for record in cur:
        for i in range(len(record) - 1):
            f.write(str(record[i]) + ",")
        f.write(str(record[-1]) + "\n")
    f.close()

def get_item_based_train_test(user_id, test_bus_id_list, train_fname, test_fname):
    test_bus_id_cnt = Counter(test_bus_id_list) # convert from a list to a counter so that later on we can
                    # do massive sorting data into train/test files more quickly
    try:
        cur.execute(item_based_command)
    except:
        print "There were problems executing the command " + item_based_command
        exit(1, "Could not execute psql command")
    f_train = open(train_fname, 'w')
    f_test = open(test_fname, 'w')
    for record in cur:
        if (record[0] == user_id and test_bus_id_cnt[record[1]] > 0):
            # if the user_id and bus_id is in the test set
            for i in range(len(record) - 1):
                f_test.write(str(record[i]) + ",")
            f_test.write(str(record[-1]) + "\n")
        else:
            # if the user_id and bus_id are in the train set
            for i in range(len(record) - 1):
                f_train.write(str(record[i]) + ",")
            f_train.write(str(record[-1]) + "\n")
    f_train.close()
    f_test.close()

