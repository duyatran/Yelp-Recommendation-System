import psycopg2
import calendar
import datetime as dt
from datetime import datetime
get_reviews_funny = "Select review_text, funny \
                    from reviews\
                    ORDER BY funny\
                    DESC\
                    LIMIT 1000;"
get_reviews_cool = "Select review_text, cool \
                    from reviews\
                    ORDER BY cool\
                    DESC \
                    Limit 1000;"
get_reviews_useful = "Select review_text, useful \
                    from reviews\
                    ORDER BY useful\
                    DESC \
                    limit 1000;"

REVIEW_COMMANDS = [get_reviews_useful, get_reviews_funny, get_reviews_cool]
REVIEW_FILE_NAMES = ["../output/useful_review.txt", "../output/funny_review.txt", "../output/cool_review.txt"]
USEFUL = 0
FUNNY = 1
COOL = 2
try:
    conn = psycopg2.connect("dbname=yelp user=vagrant")
except:
    print "Could not connect to the database yelp"
cur = conn.cursor()

def process_review(review):
    line_list = review.splitlines()
    return ''.join(line_list)

def create_review_file(what_review):
    fout = open(REVIEW_FILE_NAMES[what_review], 'w')
    try:
        cur.execute(REVIEW_COMMANDS[what_review])
    except:
        print "There were problems executing the command " + REVIEW_COMMANDS[what_review]
    for record in cur:
        processed_review = process_review(record[0])
        fout.write(processed_review + "," + str(record[1]) + "\n")
    fout.close()
create_review_file(USEFUL)
create_review_file(COOL)
create_review_file(FUNNY)
