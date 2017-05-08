import psycopg2
import re
import sets
import numpy
from collections import Counter
import macros as m
import get_item_based_input as item_based
try:
    conn = psycopg2.connect("dbname=yelp user=vagrant")
except:
    print "Could not connect to the database yelp"
cur_businesses = conn.cursor()
cur_attributes = conn.cursor()
cur_cities = conn.cursor()

def get_businesses(user_id):
    """
    :param user_id: user_id that we are trying to recommend
    :return: write out into file ./output/original/businesses_<userID>.txt the raw data of businesses' raw features
    as taken from psql
    """
    command = "SELECT stars, bus_id \
              FROM reviews \
              WHERE user_id = \'" + user_id + "\';"
    try:
        cur_businesses.execute(command)
    except:
        print "There were problems executing the command " + command
        exit(0, "PSQL Execution problem")
    #print "Done finding businesses that this user rated. Now finding their categories and attributes ..."
    f = open(m.out_dir_original + "/businesses_" + user_id + ".txt", 'w')

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
    #print "Done writing raw attributes and categories ..."
    f.close()

def write_attribute_or_categories(f, att_or_cat):
    """
    :param f: the file to write raw attributes and categories into
    :param att_or_cat: raw attribute/ categories. Attributes will be of the form attribute_name : attribute value.
    Attribute values can be True, False, any values, or even an array in and of itself
    Example: PriceRange: {'1: False', '2: True', '3: False'}, 'FreeWifi : True', etc..
    :return: write raw attribute and data in to file
    """
    if att_or_cat != None:
        for i, a_c in enumerate(att_or_cat):
            f.write(a_c + "$")
    else:
        f.write("$")

def process_sub_attribute(raw_sub_att):
    """
	Some attributes of businesses are actually arrays themselves, some are simply a string. 
	Some are actual attributes ('FreeWifi: True'), some aren't ('IndoorParking: False')
	PSQL commands are not complex enough to differentiate these and give us the exact attributes.
	This function processes a sub attribute (an attribute that has data as an array), and find out the list
	of real attributes. 
	:param: raw_sub_att: The raw text of an attribute as an array 
	:return: the text of the real attribute
	Ex: "PriceRange: {'1: False', '2: True', '3: False'}" is the raw attribute. Input of this function is 
	'1: False', output is '1'
	"""
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
    """
    :param attributes:  raw text data of bus's attributes and categories
    :return: list of clean attributes after processing the text of attributes and categories of businesses
    """
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
    """
    :param fname: Name of the file where raw data of attributes and categories taken from sql are taken
    :return: res_features : list of list of features that businesses actually have, after being cleanly processed.
             feature_set : set of features that all businesses have
             res_stars: List of users' ratings, this list indices align with the res_features mentioned above
             businesses: List of businesses id
    """
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
    #print "Done processing features and stars into binary form"
    return res_features, list(features_set), res_stars, businesses # I changed from a set to a list to make the order of elements immutable

def write_attributes_for_mc(fname, res_features, features_set, res_stars, star_threshold = m.default_star_threshold):
    """
    :param fname: the name of file to store binary data used to run machine learning models for recommendation system
    :param res_features: restaurant_features is a list of lists of features of each businesses. Each entry of the list
    is a list of features.
    :param features_set: list of features that is a union set of all features of all restaurants that we investigate
    :param res_stars: List of stars that the users rated to the restaurant. This list's indices align with ones in res_features
    , i.e. the first list of features in res_features is 1st restaurant's features, user gave the first star in res_stars
    to this restaurant.
    :param star_threshold: any restaurant that is rated above this star_threshold is considered to be liked by the user
    :return: Write binary data of resaurant feature and whether or not the user like businesses into file.
    """
    f = open(fname, 'w')
    for i, feat in enumerate(features_set):
        f.write(str(feat) + ",")
    f.write("Like?" + "\n")
    for i, res in enumerate(res_features): # For each restaurant that this user rated
        c = Counter(res_features[i])
        for j, feature in enumerate(features_set):
            f.write(str(c[feature]) + ",") # Write binary features
        if res_stars[i] >= star_threshold: # above threshold, like
            f.write(str(1) + "\n")
        else: # else, dislike
            f.write(str(0) + "\n")
    #print "Done writing attributes and ratings into binary form"
    f.close()

def write_processed_potentials(fname, res_features, features_set, businesses):
    """
    :param fname: name of file to write processed binary data of potentials' features
            res__features: list of lists of features of restaurants that user went to
            features_set: set of all features from training data
            businesses: list of businesses id as potential recommendations
    :return: write binary data of potentials' features
    """
    f = open(fname, 'w')
    f.write("bus_id,")
    for i, feat in enumerate(features_set[:-1]):
        f.write(str(feat) + ",")
    f.write(str(features_set[-1]) + "\n")
    for i, res in enumerate(res_features): # For each restaurant that this user rated
        f.write(businesses[i] + ",") # write business id
        c = Counter(res_features[i])
        for j, feature in enumerate(features_set[:-1]):
            f.write(str(c[feature]) + ",") # Write binary features
        f.write(str(c[features_set[-1]]) + "\n") # write the last feature
    #print "Done writing attributes and ratings into binary form"
    f.close()

def get_potential_recommendations(fname):
    """
    :param fname: Name of the file where raw data of attributes and categories taken from sql are taken
    :return: res_features : list of list of features that businesses actually have, after being cleanly processed.
             businesses: List of businesses id
    """
    f = open(fname, 'r')
    res_features = [] # restaurant features
    businesses = []
    for line in f:
        att_cat = line.split("|")
        attributes = att_cat[0]
        categories = att_cat[1]
        bus_id = (att_cat[2]).strip()
        features = get_attributes(attributes)
        features.extend((categories.split("$"))[:-1]) # Get rid of the last category, because due to the way we user "$", the last categories after splitting is blank
        res_features.append(features) # res_features is 2D table, [restaurant_index][attribute_index]
        businesses.append(bus_id)
    f.close()
    #print "Done processing features and stars into binary form"
    return res_features, businesses # I changed from a set to a list to make the order of elements immutable

def write_raw_potential_recommendations(cities, fname):
    """
    :param cities: A list of cities that the user has been to (has rated businesses in)
            fname: Name of file to write raw data of potential businesses
    :return: write into a file bus_ids of all businesses in that city
    """
    # Open file to write raw data of potential business attributes
    f = open(fname, 'w')
    #print "Writing raw data of cities and potential businesses for recommendation "
    # For each city that the user has been to
    for i, city in enumerate(cities):
        # Query to get all bus_ids of businesses in that city
        command = "SELECT bus_id, \
				  COALESCE (attributes, NULL) as attributes, COALESCE (categories, NULL) as categories \
                  FROM businesses \
                  WHERE  city = \'" + str(city) + "\';"
        # Execute command
        try:
            cur_cities.execute(command)
        except:
            print "There were problems executing the command " + command
            exit(0, "PSQL Execution problem")
        # Write all businesses, their attributes and categories into file businesses
        for i, att_record in enumerate(cur_cities):
            attributes = att_record[1]
            categories = att_record[2]
            write_attribute_or_categories(f, attributes)
            f.write("|")
            write_attribute_or_categories(f, categories)
            f.write("|" + str(att_record[0])) # businesses id
            f.write("\n")
    f.close()
    #print "Done"

def get_cities (bus_id_list):
    """
    :param bus_id_list: A list of businesses ids
    :return: a list of non-overlapping cities where all those input businesses reside
    """
    cities = sets.Set([])
    for i, bus_id in enumerate(bus_id_list):
        command = "SELECT city \
                  FROM businesses \
                  WHERE bus_id = \'" + bus_id + "\';"
        try:
            cur_cities.execute(command)
        except:
            print "There were problems executing the command " + command
            exit(0, "PSQL Execution problem")
        for record in cur_cities:
            cities.add(record[0])
    return list(cities)

def process_one_user_input(user_id, train_percent, star_threshold = m.default_star_threshold):
    """
    :param user_id: id of the user that we want to recommend, using 2 methods
    :param train_percent: percent of data used to train models, the rest is for testing
    :return: create files used for training and testing our original recommendation algorithm
    and for item-based algorithm
    Create files that contains potential recommendations (based on the cities that users have been to)
    """
    # 1. Open the files containing raw attributes of restaurants that this user (user_id) rated
    res_features, features_set, res_stars, businesses = \
        get_features_set_and_table(m.out_dir_original + "/businesses_" + user_id + ".txt")

    # 2. Get the index to separate train and test data
    train_index_stop = int(float(len(res_features)) * float(train_percent) / float(100))
    # 3. Write train and test data
    write_attributes_for_mc(m.out_dir_original + "/att_cat_" + user_id + "_train.txt", \
                            res_features[:train_index_stop], features_set, \
                            res_stars[:train_index_stop], star_threshold)
    #print "Done writing train data for our original methods"
    write_attributes_for_mc(m.out_dir_original + "/att_cat_" + user_id + "_test.txt", \
                                  res_features[train_index_stop:], features_set, \
                                  res_stars[train_index_stop:], star_threshold)
    #print "Done writing test data for our original methods"
    item_based_bus_exclude = businesses[train_index_stop:]
    # need to exclude this list of businesses from data in item-based, because it is used for testing
    # 4. Given the list of businesses that the users went to, find cities that the user has been to
    cities = get_cities(businesses)
    # 5. Write the cities the user has been to, adn all the businesses in those cities into file
    create_potentials_one_user(features_set, cities, user_id)
    return item_based_bus_exclude
    #print "Done writing train and test data for item_based method"

def create_potentials_one_user(pot_features_set, cities, user_id):
    """
    :param user_id:
            pot_features_set : list of features that we could find in training data, which will be used to find recommendation
            cities: list of cities that the user has been to
    :return: create 2 files, raw_bus_<userid>.txt and pot_bus_<userid>.txt that has information about features of
    potential businesses in cities that the user have been to
    """
    raw_potential_fname = m.out_dir_potential + "/raw_bus_" + user_id + ".txt"
    write_raw_potential_recommendations(cities, raw_potential_fname)
    pot_features, pot_businesses = get_potential_recommendations(raw_potential_fname)
    processed_pot_fname = m.out_dir_potential + "/pot_bus_" + user_id + ".txt"
    write_processed_potentials(processed_pot_fname, pot_features, pot_features_set, pot_businesses)

def process_all_user_input(user_fname, train_percent, star_threshold = m.default_star_threshold):
    """
    :param user_fname: the name of file that contains data of id of users that we
    want to run recommendation systems on
    :param train_percent: percent of the all businesses that the users went to that will
    be used to train the models
    :return:
    """
    user_bus_ib_test_dict = {} # dictionary keys: userid, values: counter of bus id that are used to test both models
    # (item based and original), we need this to find item-based training data and testing data
    f = open(user_fname, 'r')
    index = 0
    for line in f:
        user_id = line.strip()
        get_businesses(user_id)
        bus_ib_exclude = process_one_user_input(user_id, train_percent, star_threshold)
        user_bus_ib_test_dict[user_id] = Counter(bus_ib_exclude)
        print "Done with user " + str(index)
        index += 1
    item_based_train_fname = m.out_dir_item_based + "/train.txt"
    item_based_test_fname = m.out_dir_item_based + "/test.txt"
    item_based.get_item_based_train_test(user_bus_ib_test_dict,\
                                         item_based_train_fname,\
                                         item_based_test_fname)
    f.close()
