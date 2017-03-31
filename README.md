# COSC 480 DS Project
First, download the dataset (add instructions later)

Decompress the dataset file, the result will be several json files (and some pdfs)
        
        tar xvzf yelp_dataset_challenge_round9.tar

Install dependencies
        
        pip install psycopg2 
        pip install simplejson

Create the database
        
        createdb yelp

Create the database's schema and populate it with data.

WARNING: this will take quite a long time (about 40 minutes on my laptop). I finished my philosophy class reading while waiting for it.
        
        psql yelp -f create_yelp_dataset.sql
        python populate_db.py

(Optional) If you prefer to deal with .csv files, you can convert the json files to csv files
        
        python json_to_csv_converter.py json_file_name
