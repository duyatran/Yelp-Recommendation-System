import psycopg2
import re
import sets
import numpy
from collections import Counter
import get_item_based_input as item_based
try:
    conn = psycopg2.connect("dbname=yelp user=vagrant")
except:
    print "Could not connect to the database yelp"
cur_businesses = conn.cursor()
cur_attributes = conn.cursor()
out_dir_original = "../output/original"
out_dir_item_based = "../output/item_based"
command = "SELECT DISTINCT stars, bus_id \
FROM reviews \
WHERE user_id = 'bLbSNkLggFnqwNNzzq-Ijw'"

def get_businesses(user_id):
    command = "SELECT stars, bus_id \
              FROM reviews \
              WHERE user_id = \'" + user_id + "\';"
    try:
        cur_businesses.execute(command)
    except:
        print "There were problems executing the command " + command
        exit(0, "PSQL Execution problem")
    print "Done finding businesses that this user rated. Now finding their categories and attributes ..."
    f = open(out_dir_original + "/restaurants_" + user_id + ".txt", 'w')

    for record in cur_businesses: # For each restaurant that this user goes to, get its attributes and
        get_attributes_command = "SELECT COALESCE (attributes, NULL) as attributes, COALESCE (categories, NULL) as categories\
                                  FROM businesses \
                                  WHERE bus_id = \'" + record[1] + "\';"
        try:
            cur_attributes.execute(get_attributes_command)
        except:
            print "There were problems executing the command " + get_attributes_command
            exit(0, "PSQL Execution problem")

        for i, att_record in enumerate(cur_attributes):
            attributes = att_record[0]
            categories = att_record[1]
            write_attribute_or_categories(f, attributes)
            f.write("|")
            write_attribute_or_categories(f, categories)
            f.write("|" + str(record[0])) # write stars
            f.write("|" + str(record[1])) # write bus_id, so that we can extract information for Duy's item-based data
            f.write("\n")
            #f.write(str(att_record [0]) + "|" + str(att_record[1]) + "\n")
    print "Done writing raw attributes and categories ..."
    f.close()

def write_attribute_or_categories(f, att_or_cat):
    if att_or_cat != None:
        for i, a_c in enumerate(att_or_cat):
            f.write(a_c + "$")
    else:
        f.write("$")

def process_sub_attribute(raw_sub_att):
    sub_list = raw_sub_att.split(": ")
    att_name = re.findall(r'\'(.*?)\'', raw_sub_att)# sub attribute name needs to trim of the first and last character because they are ''
    assert  len(att_name) <= 1, "The attribute name inside \'\' must have at most one \'\'"
    if len(att_name) == 0: # If the attribute name is not inside '', as in cases where it is actually a sub attribute
        att_name = (sub_list[0]).strip()
    else:
        att_name = att_name[0]
    answer = (sub_list[1]).strip()
    if answer == "False":
        return None
    elif answer == "True":
        return att_name
    else:
        return att_name + "_" + answer

def get_attributes(attributes):
    results = []
    atts = (attributes.split("$"))[:-1] # list of attributes
    if len(atts) == 1 and atts[0] == '': # If there is no attributes (i.e attributes ="$" --> split("$") will result in  ['',''])
        return results
    for i, a in enumerate(atts): # loop through each attribute
        if "{" in a: # This attribute is a list itself
            att_name = (a[:(a.find(":"))]).strip()
            sub_att = re.findall("(?<=\{).+?(?=\})", a)
            assert len(sub_att) == 1, "There may be some thing wrong with this attribute: " + str(a)
            sub_att = (sub_att[0]).split(",") # Each sub attribute inside the {} is separated by ","
            for j, sub_a in enumerate(sub_att): # for each attribute inside {} of a attribute. Ex: Ambience: {'romantic': False, 'intimate': False}
                processed_att = process_sub_attribute(sub_a)
                if processed_att != None:
                    results.append(att_name + "_" + processed_att)
        else:
            processed_att = process_sub_attribute(a)
            if processed_att != None:
                results.append(processed_att)
    return results

def get_features_set_and_table(fname):
    f = open(fname, 'r')
    res_features = [] # restaurant features
    res_stars = [] # 1D, this user's ratings of the restaurants
    features_set = sets.Set([])
    businesses = []
    for line in f:
        att_cat = line.split("|")
        attributes = att_cat[0]
        categories = att_cat[1]
        rating_stars = att_cat[2]
        bus_id = (att_cat[3]).strip()
        features = get_attributes(attributes)
        features.extend((categories.split("$"))[:-1]) # Get rid of the last category, because due to the way we user "$", the last categories after splitting is blank
        res_features.append(features) # res_features is 2D table, [restaurant_index][attribute_index]
        features_set.update(features)
        businesses.append(bus_id)
        res_stars.append(float(rating_stars))
    f.close()
    print "Done processing features and stars into binary form"
    return res_features, list(features_set), res_stars, businesses # I changed from a set to a list to make the order of elements immutable

def write_attributes_for_mc(fname, res_features, features_set, res_stars):
    f = open(fname, 'w')
    mean_star = numpy.mean(res_stars)
    for i, feat in enumerate(features_set):
        f.write(str(feat) + ",")
    f.write("Like?" + "\n")
    for i, res in enumerate(res_features): # For each restaurant that this user rated
        c = Counter(res_features[i])
        for j, feature in enumerate(features_set):
            f.write(str(c[feature]) + ",")
        if res_stars[i] >= mean_star:
            f.write(str(1) + "\n")
        else:
            f.write(str(0) + "\n")
    print "Done writing attributes and ratings into binary form"
    f.close()

def process_attributes_catergories(user_id, train_percent):
    # 1. Open the files containing raw attributes of restaurants that this user (user_id) rated
    res_features, features_set, res_stars, businesses = get_features_set_and_table(out_dir_original + "/restaurants_" + user_id + ".txt")
    # 2. Get the index to separate train and test data
    train_index_stop = int(float(len(res_features)) * float(train_percent) / float(100))
    # 3. Write train and test data
    write_attributes_for_mc(out_dir_original + "/att_cat_" + user_id + "_train.txt", \
                            res_features[:train_index_stop], features_set, \
                            res_stars[:train_index_stop])
    print "Done writing train data for our original methods"
    write_attributes_for_mc(out_dir_original + "/att_cat_" + user_id + "_test.txt", \
                                  res_features[train_index_stop:], features_set, \
                                  res_stars[train_index_stop:])
    print "Done writing train data for our original methods"
    test_bus = businesses[train_index_stop:]
    # Given the user ide and businesses id used to test, write data to train and test item_baed model
    item_based.get_item_based_train_test(user_id, test_bus, \
                                         out_dir_item_based + '/trainData.txt', \
                                         out_dir_item_based + '/testData.txt')
    print "Done writing train and test data for item_based method"

#get_businesses('CxDOIDnH8gp9KXzpBHJYXw')
process_attributes_catergories('CxDOIDnH8gp9KXzpBHJYXw', 70)
