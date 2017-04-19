from collections import defaultdict
import csv

# the below shell command is used to 
# psql yelp -A -t --variable="FETCH_COUNT=10000" -c "select categories from businesses" > categories.txt
# Delete all occurances of '{', '}' and double quotes character 
# sed 's/[{}"]//g' categories.txt > output.txt

categories = defaultdict(int)

### get the 10000 bus_id, num_check_ins that have the highgest num check ins
def write_to_file():
    with open('../../output/output.txt', 'rb') as fin, open('../../output/categories_count.csv','w') as fout:
        for line in fin:
            cats = line.split(',')
            for cat in cats:
                cat = cat.strip()
                categories[cat] += 1
        writer = csv.DictWriter(fout, ['Category','Count'])
        writer.writeheader()
        for category, count in categories.iteritems():
            writer.writerow({'Category': category, 'Count': count})

write_to_file()