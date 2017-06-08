# Yelp Recommendation System
We used data made public for educational purposes by Yelp Inc.. To motivate students and researchers in their pursuits of developments of better algorithms and practices in tackling big and complex data, Yelp created public challenges by publishing a part of their data and challeng scholars and curious minds to find meanings in their wealth of data. The data we downloaded from Yelp is 4.98GB; we used data from round 9 challenge. The link to the data is: https://www.yelp.com/dataset_challenge
# 1. Item-based collaborative filtering
Collaborative filtering is a recommender system technique that makes predictions about the interests of a user by collecting preferences or taste information (in our case, rating or number of stars a user gives a business) from many users. This can either be done by (1) computing similar users (user-based), or (2) computing similar items (item-based). Maintaining a user-user similarity matrix is more computationally expensive than an item-item similarity matrix, so we choose to the latter: in this case, we have 1,029,432 users and 144,072 businesses.
Similarity measures include Jaccard similarity, Cosine similarity and Pearson Correlation similarity. We choose to use Pearson Correlation similarity because our data has explicit ratings (while Jaccard is good for implicit rating case), and it also removes effects of means and variance (unlike Cosine). Source and more information can be found here.
Since item-based collaborative filtering is an established technique, we want to use it as a reference for comparison with our original method, and so we use a third library instead of trying to implement it ourselves. Our textbook recommends Crab but we had trouble importing and using it, not to mention it has been abandoned for a few years. We then tried out LightFM and Surprise before settling on the latter because it implements item-based collaborative filtering and is easy to use. Surprise turns out to be surprisingly bad, as its algorithm seems ill-designed for larger-than-memory amount of data. We keep running into MemoryError because of codes like sq_diff = np.zeros((n_x, n_x), np.double) (n_x being the number of 144,072 businesses) which create huge 2-D arrays in memory and so crash. We then switched to GraphLab (instructions to install in README), which works great with one caveat: it requires a minimum of 4 GB of RAM. Our VM as defined by Vagrantfile has 2 GB RAM, and that could cause the process to take a long time or killed by the Linux kernal. After increasing it to 4 GB, the training process ran in just 1 minute.
To make test statistics (accuracy and precision-recall) comparable between the two methods, we do not use builtin evaluate_precision_recall or recommend functions provided by GraphLab, but we wrote our own. This is because the builtin item-based model predicts non-binary rating, while our method recommends based on a binary rating (like/dislike), so we convert predicted rating to binary rating (1 for like, 0 for dislike) and then calculate accuracy, precision-recall based on that.
To make recommendation lists comparable, we integrate our potentials into the item-based model as follows: we run item_based_model.predict(potentials) to predict the scores for the potentials, set the threshold at 4 and output all businesses with at least 4-star predicted rating. Potential businesses are defined to be businesses in the cities the user had had reviews in.
This method works as followed:
Input: a user list, e.g. [a,b]
Train data: all users' ratings, except for the "test" parts (a_test, b_test)
Test data: a_test, b_test (same with the our original method)
Output: one accuracy file for all users, one precision-recall file for all users, and one recommendation list file per user. The format of these files are similar to the ones described in the next section.
# 2. Our original recommendation method
Our original recommendation system predicts businesses a user X will like based on X's reviews. First, we feed our algorithm a list of X's past business reviews in a csv file. Each business review includes a list of binary attributes which indicates whether the business is in certain categories. For instance. McDonald might have a list of attributes such as "fastFood", "shopping" and "spa", so it will have a 1 for "fastFood" indicating it is a fast food resteurant and have 0 for both "shopping" and "spa". Each business also has a binary attribute "like" showing whether x likes the business or not. It is also the target attribute of our model. Yelp users can rate businesses from 1 to 5, with 5 being the best rating. We set a threshold of 4, so if x gives a business 4 to 5 stars, we say X likes it, so set the "like" attribute for the business to be 1, and 0 otherwise.
Given a list of business reviews by X, we split the list into trainData and testData. We use the trainData to train on Decision Tree, Logistic Regression and Naive Bayes models. We then test each model's accuracy with our testData and write them to a file. Along the process we also calculate each model's precision score and recall score for comparison purpose later. Each user will be recorded as one row in the accuracy and precision_recall file and the format of accuracy file will be:
userID	Decision Tree	Logistic Regression	Naive Bayes
x	54.7309833	56.95732839	43.41372913
y	62.06206206	66.36636637	38.23823824
...	...	...	...
The format of precision_recall file will be:
userID	DT_precision	DT_recall	LR_precision	LR_recall	NB_precision	NB_recall
x	0.375586854	0.418848168	0.262910798	0.427480916	0.887323944	0.40212766
y	0.396969697	0.421221865	0.260606061	0.483146067	0.857575758	0.857575758
...	...	...	...	...	...	...
After computing accuracy and precision-recall scores, we choose the model with the highest accuracy and use it to recommendate businesses. For instance, given the input to be a list of potential businesses and the model to be decision tree, we feed all the potential businesses to decision tree model and only output the ones the user X likes("like" attribute is predicted to be 1). Each potential business also has a list of binary attributes as business reviews discussed above, but it does not have "like" attribute since we are predicting user preferences. At the end our system will generate a file containing all the businesses user X likes out of the potential businesses. The file will look like:
McDonald
Slices
Frank
...
# Instructions
- First, download the Yelp data from https://www.yelp.com/dataset_challenge/dataset. You will find a compressed file in your Downloads folder. Uncompress it (tar xvzf yelp_dataset_challenge_round9.tar), name the folder 'yelp_data', and move it into the directory of this project (It has to be in the same level as the source folder, i.e. not inside the source folder).

- Second, install dependency for this project: 
        pip install psycopg2 
        pip install simplejson

- Third, navigate into source folder and create the Yelp dataset by running create_yelp_dataset.sql: 
        createdb yelp
        psql yelp -f create_yelp_dataset.sql
        
  The schema of this database are can be viewed create_yelp_dataset.sql. We made some modifications to the general structure of database given from Yelp. Most arrays are pulled out to create new tables to take advantage of indexing.
  
  Populate the database with data. WARNING: The time it takes to import data from json files to local database is 40 mins-60 mins: 
        python populate_db.py

- Next, register for a license of GraphLab at https://turi.com/download/academic.html and install GraphLab (more info [here](https://turi.com/download/install-graphlab-create-command-line.html)):
        pip install --upgrade --no-cache-dir https://get.graphlab.com/GraphLab-Create/2.1/your-registered-email-address-here/your-product-key-here/GraphLab-Create-License.tar.gz

- Change Vagrantfile setting, line 54 to `v.memory = 4096` to give the VM 4 GB of RAM (you can allocate more for faster results, if your machine has RAM to spare). This is necessary for GraphLab to run at all.
