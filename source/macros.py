out_dir = "../output"
out_dir_original = "../output/original"
out_dir_item_based = "../output/item_based"
out_dir_potential = "../output/potentials"
out_dir_users = "../output/users"
out_dir_results = "../output/results"
item_based_fname = out_dir_item_based + "/all_input.txt"
user_more_thres_fname = out_dir_users + "/users_more_"
user_limit = out_dir_users + "/users_limit_" # Have to add the limit threshold and txt afterward

def get_user_more_thres_fname(threshold):
    """

    :param threshold: If users has number of reviews above this threshold,
    their user_id should be recorded into a file whose name created by this function
    :return:
    """
    return user_more_thres_fname + str(threshold) + ".txt"

def get_user_limit_fname(limit):
    """
    :param limit: The number of users to pick id from
    :return: the file name to store ideal user_ids
    """
    return user_limit + str(limit) + ".txt"