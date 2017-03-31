import psycopg2
import calendar
import datetime as dt
from datetime import datetime
import simplejson as json

day_abbr = list(calendar.day_abbr) # ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
day_name = list(calendar.day_name) # ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

conn = psycopg2.connect("dbname=yelp user=vagrant")
cur = conn.cursor()

def populate_businesses():
    with open('yelp_academic_dataset_business.json') as f:
        for line in f:
            line_content = json.loads(line)
            bus_id = line_content['business_id']
            bus_name = line_content['name']
            neighborhood = line_content['neighborhood']
            address = line_content['address']
            city = line_content['city']
            state = line_content['state']
            postCode = line_content['postal_code']
            latitude = float(line_content['latitude'])
            longitude = float(line_content['longitude'])
            stars = float(line_content['stars'])
            review_count = int(line_content['review_count'])
            is_open = True if line_content['is_open'] == 1 else False
            attributes = line_content['attributes']
            categories = line_content['categories']

            cur.execute("INSERT INTO businesses (bus_id, bus_name, neighborhood, address, city, state, postCode, latitude, longitude, stars, review_count, is_open, attributes, categories) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (bus_id, bus_name, neighborhood, address, city, state, postCode, latitude, longitude, stars, review_count, is_open, attributes, categories))

def extract_business_hours(time):
    day, open_close = time.split(' ')
    day_int = day_name.index(day)
    open_time, close_time = open_close.split('-')
    open_time_h, open_time_m = open_time.split(':')
    close_time_h, close_time_m = close_time.split(':')

    return (day_int, dt.time(int(open_time_h), int(open_time_m)), dt.time(int(close_time_h), int(close_time_m)))

def populate_business_hours():
    with open('yelp_academic_dataset_business.json') as f:
        for line in f:
            line_content = json.loads(line)
            bus_id = line_content['business_id']
            if (line_content['hours'] != None):
                for time in line_content['hours']:
                    day, open_time, close_time = extract_business_hours(time)
                    cur.execute("INSERT INTO business_hours (bus_id, day, open_time, close_time) VALUES (%s, %s, %s, %s)", (bus_id, day, open_time, close_time))

def extract_checkin_time(time):
    day, hour_count = time.split('-')
    day_int = day_abbr.index(day)
    hour, count = hour_count.split(':')
    return (day_int, int(hour), int(count))

def populate_checkin():
    with open('yelp_academic_dataset_checkin.json') as f:
        for line in f:
            line_content = json.loads(line)
            bus_id = line_content['business_id']
            for time in line_content['time']:
                day, hour, count = extract_checkin_time(time)
                cur.execute("INSERT INTO check_ins (bus_id, day, hour, count) VALUES (%s, %s, %s, %s)", (bus_id, day, hour, count))

def populate_users():
    with open('yelp_academic_dataset_user.json') as f:
        for line in f:
            line_content = json.loads(line)
            user_id = line_content['user_id']
            name = line_content['name']
            review_count = int(line_content['review_count'])
            yelp_since = datetime.strptime(line_content['yelping_since'], '%Y-%m-%d')
            friends = line_content['friends']
            useful = int(line_content['useful'])
            funny = int(line_content['funny'])
            cool = int(line_content['cool'])
            fans = int(line_content['fans'])
            avg_stars = float(line_content['average_stars'])
            compliment_hot = int(line_content['compliment_hot'])
            compliment_more = int(line_content['compliment_more'])
            compliment_profile = int(line_content['compliment_profile'])
            compliment_cute = int(line_content['compliment_cute'])
            compliment_list = int(line_content['compliment_list'])
            compliment_note = int(line_content['compliment_note'])
            compliment_plain = int(line_content['compliment_plain'])
            compliment_cool = int(line_content['compliment_cool'])
            compliment_funny = int(line_content['compliment_funny'])
            compliment_writer = int(line_content['compliment_writer'])
            compliment_photos = int(line_content['compliment_photos'])

            cur.execute("INSERT INTO users (user_id, name, review_count, yelp_since, friends, useful, funny, cool, fans, avg_stars, compliment_hot, compliment_more, compliment_profile, compliment_cute, compliment_list, compliment_note, compliment_plain, compliment_cool, compliment_funny, compliment_writer, compliment_photos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (user_id, name, review_count, yelp_since, friends, useful, funny, cool, fans, avg_stars, compliment_hot, compliment_more, compliment_profile, compliment_cute, compliment_list, compliment_note, compliment_plain,compliment_cool, compliment_funny, compliment_writer, compliment_photos))

def populate_elite_users():
    with open('yelp_academic_dataset_user.json') as f:
        for line in f:
            line_content = json.loads(line)
            user_id = line_content['user_id']
            if line_content['elite'] != ['None']:
                for year in line_content['elite']:
                    cur.execute("INSERT INTO elite_users (user_id, year) VALUES (%s, %s)", (user_id, year))

def populate_reviews():
    with open('yelp_academic_dataset_review.json') as f:
        for line in f:
            line_content = json.loads(line)
            review_id = line_content['review_id']
            user_id = line_content['user_id']
            bus_id = line_content['business_id']
            stars = float(line_content['stars'])
            review_date = datetime.strptime(line_content['date'], '%Y-%m-%d')
            review_text = line_content['text']
            useful = int(line_content['useful'])
            funny = int(line_content['funny'])
            cool = int(line_content['cool'])

            cur.execute("INSERT INTO reviews (review_id, user_id, bus_id, stars, review_date, review_text, useful, funny, cool) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (review_id, user_id, bus_id, stars, review_date, review_text, useful, funny, cool))

def populate_tips():
    with open('yelp_academic_dataset_tip.json') as f:
        for line in f:
            line_content = json.loads(line)
            tip_text = line_content['text']
            user_id = line_content['user_id']
            bus_id = line_content['business_id']
            tip_date = datetime.strptime(line_content['date'], '%Y-%m-%d')
            likes = int(line_content['likes'])

            cur.execute("INSERT INTO tips (tip_text, tip_date, likes, bus_id, user_id) VALUES (%s, %s, %s, %s, %s)", (tip_text, tip_date, likes, bus_id, user_id))

# Tried creating a "friends" relation out of the user json file. It took forever, so keep friends as an array in users.
# def populate_friends():
#     with open('yelp_academic_dataset_user.json') as f:
#         for line in f:
#             line_content = json.loads(line)
#             user_id1 = line_content['user_id']
#             for friend in line_content['friends']:
#                 print user_id1
#                 print friend
#                 cur.execute("INSERT INTO friends (user_id1, user_id2) VALUES (%s, %s)", (user_id1, friend))

# Cannot populate business_hours or check_ins table simultaneously with businesses table, because FOREIGN KEY REFRENCE constraint requires bus_id to exist in businesses before allowing insertion of that bus_id's row into business_hours and check_ins. Same with users and other tables.
populate_businesses()
populate_checkin()
populate_business_hours()
populate_users()
populate_elite_users()
populate_reviews()
populate_tips()

conn.commit()
cur.close()
conn.close()