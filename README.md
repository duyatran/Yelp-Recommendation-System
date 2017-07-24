# Yelp Recommendation System
This project used data made public for educational purposes by Yelp Inc. The data (and its schema) is from the Yelp Dataset Challenge Round 9, and could be obtained [here](https://www.yelp.com/dataset_challenge) (4.98GB). The goal of this project is to use Machine Learning algorithms to create a business recommendation system for Yelp users that hopefully can outperform classic item-based collaborative filtering algorithm.

# 1. Item-based collaborative filtering
Collaborative filtering is a recommender system technique that makes predictions about the interests of a user by collecting preferences or taste information (in our case, rating or number of stars a user gives a business) from many users. This can either be done by 

(1) computing similar users (user-based) or,

(2) computing similar items (item-based). 

In this case, we have 1,029,432 users, but only 144,072 businesses. Maintaining a user-user similarity matrix is more computationally expensive than an item-item similarity matrix, so we choose to the latter.

Similarity measures include Jaccard similarity, Cosine similarity and Pearson Correlation similarity. We choose to use Pearson Correlation similarity because our data has explicit ratings (while Jaccard is good for implicit rating s), and it also takes into account a user's means and variance of ratings (unlike Cosine). Source and more information can be found [here](https://turi.com/products/create/docs/generated/graphlab.recommender.item_similarity_recommender.ItemSimilarityRecommender.html#graphlab.recommender.item_similarity_recommender.ItemSimilarityRecommender).

Since item-based collaborative filtering is an established technique, we want to use it as a reference for comparison with our original method, and so we use a third library instead of trying to implement it ourselves. We tried using [Surprise](http://surpriselib.com/), but it turns out to be surprisingly bad, as its algorithm seems ill-designed for larger-than-memory amount of data. We keep running into MemoryError because of snippets of code that try to create huge 2-D arrays in memory and so crash and burn. 
```python
# n_x being the number of 144,072 businesses 
sq_diff = np.zeros((n_x, n_x), np.double)
``` 
We then switched to [GraphLab](https://turi.com/), which works great (it does require a minimum of 4 GB of RAM).

To make test statistics (accuracy and precision-recall) comparable between GraphLab's item-based filtering and out method, we do not use built-in `evaluate_precision_recall()` or `recommend()` functions provided by GraphLab, but we wrote our own. This is because the built-in item-based model predicts non-binary ratings, while our method recommends based on a binary rating (like/dislike), so we had to convert GraphLab's predicted ratings to binary ratings (1 for like, 0 for dislike) and then calculate accuracy & precision-recall based on that.

To make recommendation lists comparable, we integrate our potentials (i.e. list of business we could potentially recommend to a particular user) into the item-based model as follows: we run item_based_model.predict(potentials) to predict the scores for the potentials, set the threshold at 4 and output all businesses with at least 4-star predicted rating. Potential businesses are defined to be businesses in the cities the user had had reviews in.

This method works as followed:
* Input: a user list, e.g. [a,b]
* Train data: all users' ratings, except for the "test" parts (a_test, b_test)
* Test data: a_test, b_test (same with the our original method)
* Output: one accuracy file for all users, one precision-recall file for all users, and one recommendation list file per user. The format of these files are similar to the ones described in the next section.

# 2. Our original recommendation method

Our original recommendation system predicts businesses a user X could like by building a model of X's preferences of the business attributes based on X's previous reviews. It is, in some way, a content-based filtering technique.

First, we feed our algorithm a list of X's past business reviews in a csv file. Each business review includes a list of binary attributes. For instance. McDonald might have a list of attributes such as "fastFood", "shopping" and "spa", so it will have a 1 for "fastFood" indicating it is a fast food resteurant and have 0 for both "shopping" and "spa". Each business also has a binary attribute "like" showing whether X likes the business or not. It is also the target attribute of our model. Yelp users can rate businesses from 1 to 5, with 5 being the best rating. We set a threshold of 4, so if X gives a business 4 to 5 stars, we say X likes it and set the "like" attribute for the business to be 1, and 0 otherwise.

Given a list of business reviews by X, we split the list into trainData and testData. We use the trainData to train on Decision Tree, Logistic Regression and Naive Bayes models. We then test each model's accuracy with our testData and write them to a file. Along the process we also calculate each model's accuracy & precision-recall statistic for comparison purpose later. Each user will be recorded as one row in the accuracy and precision_recall file and the format of accuracy file will be:

|userID|Decision Tree|Logistic Regression|Naive Bayes|
| ------------- |:-------------:| -----:| ---:|
|x | 54.7309833  |  56.95732839| 43.41372913|
|y | 62.06206206  |  66.36636637 | 38.23823824|
|...|...|...|...|


The format of precision_recall file will be:

|userID|DT_precision|DT_recall|LR_precision|LR_recall|NB_precision|NB_recall|
| ------------- |:-------------:| -----:| ---:|------:|----:|-----:|
|x    | 0.375586854| 0.418848168 |0.262910798|0.427480916|0.887323944|0.40212766|
|y     | 0.396969697| 0.421221865 |0.260606061|0.483146067|0.857575758|0.857575758
|... | ...      |    ... |...|...|...|...|

After computing accuracy and precision-recall scores, we choose the model with the highest accuracy and use it to recommend businesses. For instance, given the input to be a list of potential businesses and the model to be decision tree, we feed all the potential businesses to decision tree model and only output the ones the user X likes ("like" attribute is predicted to be 1). Each potential business also has a list of binary attributes as business reviews discussed above, but it does not have "like" attribute since we are predicting user preferences. At the end our system will generate a file containing all the businesses user X likes out of the potential businesses. The file will look like:

McDonald

Slices

Frank

...

# Results
Please see our final presentation or the figures in the repo folder plots_to_git for the accuracy histograms, precision histograms and the recall histograms. Because of the long time it takes to get input for users (for each user, we had to write down to a file a list of potentials, and train & test data for that user from the database), we could only run a test on 35 users with the highest number of reviews. The results below are the performance comparison between our method and the item-based model on the test data, based on three measurements: accuracy, precision, and recall.

The results shown in 35 user models’ accuracies of both our method and the item-based method. We train three models (decision tree, naive Bayes and logistic regression) for each user for our method but take the one with the highest accuracy to compare with the item-based method. Accuracy is essentially the percentage of predictions by the model that are correct. Based on the histogram above, we can observe that our method generates most model accuracies around 55% to 65%, while the item-based method has the most accuracies around 60% to 70%. It seems that the item-based method outperforms our method based on accuracy.

Precision is, in our context, the fraction of businesses the user actually likes out of the ones we predict that the user would like, so the closer a precision is to 1, the better the model is. Based on the precision histograms above, we can find that our model slightly beat the item-based model with more than 21 models’ precision scores above 80%, while only 16 models out of the item-based method have the scores above 80%. It suggests that our model select more businesses that the user actually likes compared to the item-based model.

Recall (also known as sensitivity) is the fraction of businesses that we predict the user would like out of the total number of businesses that the user actually likes. It seems that our method clearly outperforms the item-based model on recall scores. Our method has 12 models exceeding 80% recall score while the number for the item-based score is only 2. The results suggest that our method is able to capture more of the businesses a user actually likes than the item-based method, indicating a strong predictability of our method.

# Evaluation
Notes/Limitations of our project include:

* Duplicates of potentials and reviews: we do not exclude businesses a user had reviewed from that user's list of potential recommendations, due to time constraint.

* To make the two methods comparable, we do not use item-based model's built-in recommend() function, and instead find predicted ratings on potentials and use the same threshold as our method's to make the 'rating' binary. This makes the item-based method's less fine-grained than it is by default, because (1) it recommends some duplicates between potentials and reviews (see above), and (2) by converting 1-5 rating to a binary variable, we lose a lot of data and cannot really distinguish which businesses a user likes more than the others.

* Both methods are bare-bone implementations, and there are a lot of room for improvement. For example, no feature engineering is done on the models in our method, and due to the small amount of data, we decided not to do cross validation.

* We were too dependent to our PostgreSQL database and Python DB API that we wrote all of our input processing (for the two models) through the database. One major limitation of this approach is that it might have taken longer than it needs to get a user's input, and so limiting our sample size to evaluate the two models (i.e. we only had time to run the comparison for 35 users). In retrospect, we could have looked into getting the input data straight out of the JSON files, which we guess could be faster than executing queries on the database through Python's DB API.

* We did not get the chance to test both models on users with few reviews, so we could not draw any conclusion about those users.

* As alluded to before, because of our sample size used in evaluation (35 users), the observations in the "Results" section are by no means conclusive that our model actually outperforms the item-based model.

# Instructions
- First, download the Yelp data from [here](https://www.yelp.com/dataset_challenge/dataset) and decompress it:
```
tar xvzf yelp_dataset_challenge_round9.tar
```
  Name the folder 'yelp_data', and move it into the directory of this project (It has to be in the same level as the source folder, i.e. not inside the source folder).

- Second, install dependency for this project: 
```
pip install psycopg2 
pip install simplejson
```

- Third, navigate into source folder and create the Yelp database by running create_yelp_dataset.sql: 
```
createdb yelp
psql yelp -f create_yelp_dataset.sql
```        
  The schema of this database are can be viewed create_yelp_dataset.sql. We made some modifications to the general structure of database given from Yelp. Most arrays are pulled out to create new tables to take advantage of indexing.
  
  Populate the database with data. WARNING: The time it takes to import data from json files to local database is 40 mins-60 mins:
```
python populate_db.py
```

- Next, [register for a license](https://turi.com/download/academic.html) of GraphLab and install GraphLab (more info [here](https://turi.com/download/install-graphlab-create-command-line.html)):
```
pip install --upgrade --no-cache-dir https://get.graphlab.com/GraphLab-Create/2.1/your-registered-email-address-here/your-product-key-here/GraphLab-Create-License.tar.gz
```

- Please follow section **III. Methods** in [finalReport](https://github.com/colgate-cosc480ds/project-duy-ha-pj/blob/master/source/finalReport.ipynb) to set up inputs and test out two recommendation methods.