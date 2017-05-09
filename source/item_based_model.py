import graphlab
import csv
import macros as m

TRAIN_DATA_PATH = m.out_dir_item_based + '/train.txt'

def run(user_fname):
    train_data = graphlab.SFrame.read_csv(TRAIN_DATA_PATH)
    item_based_model = graphlab.item_similarity_recommender.create(train_data, user_id='user_id',
                                                                   item_id='bus_id', target='rating',
                                                                   similarity_type='pearson')

    with open(user_fname, 'rb') as user_file, open(m.out_dir_results + "/item_based_accuracy.csv", "a+") as f:
        writer = csv.DictWriter(f, ['user_id', 'accuracy', 'precision', 'recall'])
        writer.writeheader()

        for user in user_file:
                user = user.strip()
                #user = "CxDOIDnH8gp9KXzpBHJYXw"
                potentials = graphlab.SFrame.read_csv(m.out_dir_potential + '/pot_bus_' + user + '.txt')
                test_set_path = m.out_dir_item_based + '/test_' + user + '.txt'
                test_data = graphlab.SFrame.read_csv(test_set_path)

                # predict on test data
                pred = item_based_model.predict(test_data)
                test_data = test_data.add_column(pred, name='predicted_rating')

                #lambda func below transform a predicted score to the nearest .5, e.g. 3.99 -> 4.00, so 4.0 does not
                # need to be "hard" threshold
                binary_rating = test_data.select_column('rating').apply(lambda x: 0 if (round(x * 2) / 2.0) < 4.0 else 1, dtype=int)
                binary_pred = test_data.select_column('predicted_rating').apply(lambda x: 0 if (round(x * 2) / 2.0) < 4.0 else 1, dtype=int)

                correct_count = 0
                true_positive = 0
                positive_pred = 0
                positive_rating = 0
                for i in range(len(binary_rating)):
                    if binary_pred[i] == binary_rating[i]:
                        correct_count += 1.0
                    if binary_rating[i] == 1 and binary_pred[i] == 1:
                        true_positive +=  1.0
                    if binary_pred[i] == 1:
                        positive_pred += 1.0
                    if binary_rating[i] == 1:
                        positive_rating += 1.0
                accuracy = correct_count / len(binary_rating) * 100
                precision = true_positive / positive_pred * 100
                recall = true_positive / positive_rating * 100

                # write accuracy and precision_recall to test_data

                writer.writerow({'user_id': user,
                                 'accuracy': accuracy,
                                 'precision': precision,
                                'recall': recall})

                # make recommendations based on potentials
                #item_based_recomm = item_based_model.recommend(users=[user], k=25)
                #item_based_recomm.print_rows()

                # predict on potentials
                # potentials need to look like train.txt for predict to work
                # so first, add a dummy rating 'rating' column, and add a 'user_id' column.
                # results will not be affected
                potentials.add_column(graphlab.SArray(data=[0 for x in range(len(potentials))]), name='rating')
                potentials = potentials.select_columns(['bus_id','rating'])
                potentials.add_column(graphlab.SArray(data=[user for x in range(len(potentials))]), name='user_id')

                # predict on potentials and filter out ones with predicted_rating >=4
                potential_pred = item_based_model.predict(potentials)
                potentials = potentials.add_column(potential_pred, name='predicted_rating')

                recs = potentials[potentials['predicted_rating'] >= 4.0]
                recs_csv = graphlab.SFrame({'bus_recommended': recs['bus_id']})
                recs_csv.export_csv(m.out_dir_results + "/item_based_result_" + user + ".csv")

if __name__ == "__main__":
    run(m.get_user_more_thres_fname(1000))
