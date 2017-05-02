# Weekly Status Reports

Each week, please spend 5-10 minutes writing a brief status report.  This does not need to be highly detailed. Some examples are provided below that give some indication of the level of detail.

*Copy the template below for each subsequent week.  Please put the most recent week at the **TOP** of the page.*

## Week 5

#Report for the week of 04/18/2017 to 04/24/2017.
* After talking to Professor Hay, we decided to also look into well-known methods used by established recommender system, such as user-based and item-based collaborative filtering. The plan now is to implement our approach and a collaborative filtering approach, then compare the performance of the two.
* Duy: I was tasked with looking into Crab, a prominent Python framework for collaborative filtering.The Crab project, however, has been abandoned, so I looked into alternatives. I wrote some test code to compare three frameworks Crab, LibRec, and Surprise (previously known as RecSys). I decide to pick Surprise because of the clean and easy-to-use API and its good variety of collaborative filtering (and other) algorithms.   
* Ha: This week I will start working on our approach. Given a user_id, I will get the data ready for the subsequent machine learning step.
* Drew: I will assume I have the data input from Ha's work, and so work on running ML algorithms (maybe with cross-validation) on input data.

## Week 4

#Report for the week of 04/11/2017 to 04/17/2017.
* Drew joined us in the middle of the week but he had no access to the github repo, and Ha had some problems with her git settings so coordination was through a Google Drive folder.
* This week we all discussed to flesh out the details of our recommender system approach. We decide to go ahead with our approach of "training ML models on user's ratings, then use it to give recommendations," because there are quite a lot of users with substantial number of ratings (e.g. >1000 users with >1000 ratings)
* Duy: This week I also wrote scripts to pull out relevant data for our visualizations and put together the mini-presentation.
* Ha: This week I refined my graphs and worked with Drew on the visualizations and Duy on the mini-presentation.
* Drew: This week I watched Tableau tutorials and produced the visualizations for the mini-presentation.

#Work distribution:
* Duy: 33.3 %
* Ha: 33.3 %
* Drew: 33.3 %

## Week 3

#Report for the week of 04/04/2017 to 04/10/2017.
* Duy: This week was a hectic week for me, so I did not get much work done. I discussed with Ha about the possibility of writing a recommender system for users based on their reviews and wrote up a rough outline of our approach (idea.txt in ./source folder).
* Ha: This week I did some data exploration to find potential interesting trends/patterns/questions we can answer. I also plotted some stuff that I found interesting:
1. Average number of check-ins per week per business for the top 10 cities with the most check-ins.
2. Spatial distribution of businesses in all cities in the dataset. I figure I may find something interesting about the 

#Work distribution:
* Duy: 30 %
* Ha: 70 %

## Week 2

#Report for the week of 03/28/2017 to 04/03/2017.
* Duy: This week I created the schema and wrote scripts to populate the postgresql database from the Yelp dataset that we downloaded from https://www.yelp.com/dataset_challenge/. I also found a script to convert json to csv files if need be.
* Ha: This week I worked on doing some data retrieving from the database that Duy created. In particular, the two worthwhile things that I collected are:
1. Files of the 1000 most funny/cool/useful (most funny/cool/useful votes) reviews. We were trying to answer a question suggested by the competition
description: "What makes a review funny/cool/useful?". We plan to do some text mining stuff with it.
2. Files of the accumulative data about the checked-in times of the weeks for the 10 cities with the most check-ins. I will draw histogram plots for each of these 10 cities to see, for each city, the most popular times.

#Work distribution:
* Duy: 50 %
* Ha: 50 %

## Week 1

Report for the week of 3/20/17 to 3/27/17.

We worked on choosing a good project for this week, but on Tuesday 03/28/2017 we had to change because our data is not big enough. Therefore, this week does not count any more.
