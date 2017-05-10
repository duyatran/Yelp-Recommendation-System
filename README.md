# COSC 480 DS Project
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