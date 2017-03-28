-- drop the tables if they already exist

DROP TABLE IF EXISTS business CASCADE;
DROP TABLE IF EXISTS check_in CASCADE;
DROP TABLE IF EXISTS review CASCADE;
DROP VIEW IF EXISTS tip CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- create the tables and views
-- note: primary keys and foreign keys are specified at the end of this file
-- (indexes created after data is loaded)


-- business
CREATE TABLE business (
    bus_id character(100) NOT NULL ,
    bName CHARACTER (200),
    neighborhood CHARACTER (200),
    address CHARACTER (200),
    city CHARACTER (200),
    state CHARACTER (15),
    postCode CHARACTER (10),
    latitude double,
    longitude DOUBLE ,
    stars DOUBLE ,
    review_count INTEGER ,
    is_open boolean,
    attributes NULL, -- an array of strings: each array element is an attribute
    catergories NULL, -- an array of strings of business categories
    hours NULL, -- an array of strings of business hours
);


-- check-ins
CREATE TABLE check_in (
  bus_id character(100) NOT NULL,
);



CREATE TABLE users (
    user_id character(100) NOT NULL,
    name character(20) NOT NULL,
    review_count INTEGER NOT NULL,
    yelp_since date NOT NULL, -- format like 2009-12-19
    friends NULL,-- Arrays of friends ID
    useful INTEGER , -- number of useful votes sent by the user
    funny INTEGER , -- number of funny votes sent by the user
    cool INTEGER , -- number of cool votes sent by the user
    fans INTEGER , -- number of fans the user has
    elite NULL, -- array of years that the user was elite
    avg_stars DOUBLE , -- floating points
    compliment_hot INTEGER , -- number of hot compliments received by the user
    complement_more INTEGER , -- number of more compliments received by the user
    complement_profile INTEGER , -- number of profile compliments received by the user
    complement_cute INTEGER , -- number of cute compliments received by the user
    complement_list INTEGER , -- number of list compliments received by the user
    complement_note INTEGER , -- number of note compliments received by the user
    complement_plain INTEGER , -- number of plain compliments received by the user
    complement_cool INTEGER , -- number of cool compliments received by the user
    complement_funny INTEGER , -- number of funny compliments received by the user
    complement_writer INTEGER , -- number of writer compliments received by the user
    complement_photoes INTEGER  -- number of photos compliments received by the user

);

CREATE TABLE review (
    review_id character(100) NOT NULL,
    user_id character(100) NOT NULL,
    bus_id character(100) NOT NULL ,
    stars DOUBLE ,
    rDate DATE ,
    text CHARACTER (2000),
    useful INTEGER , -- number of useful votes received
    funny INTEGER , -- number of funny votes received
    cool INTEGER  -- number of cool votes received
);

CREATE TABLE tip (
  text CHARACTER (2000),
  tDate DATE , -- format like 2009-12-19
  likes INTEGER , -- Compliment count
  bus_id CHARACTER (100),
  user_id CHARACTER (100)
);



-- load the data

COPY bills FROM '/vagrant/lab3/bills.csv' WITH
(FORMAT csv, HEADER true, DELIMITER ',');
COPY person_roles FROM '/vagrant/lab3/person_roles.csv' WITH
(FORMAT csv, HEADER true, DELIMITER ',');
COPY persons FROM '/vagrant/lab3/persons.csv' WITH
(FORMAT csv, HEADER true, DELIMITER ',');
COPY person_votes FROM '/vagrant/lab3/person_votes.csv' WITH
(FORMAT csv, HEADER true, DELIMITER ',');
COPY states FROM '/vagrant/lab3/states.csv' WITH
(FORMAT csv, HEADER true, DELIMITER ',');
COPY votes FROM '/vagrant/lab3/votes.csv' WITH
(FORMAT csv, HEADER true, DELIMITER ',');
COPY votes_re_amendments FROM '/vagrant/lab3/votes_re_amendments.csv' WITH
(FORMAT csv, HEADER true, DELIMITER ',');
COPY votes_re_bills FROM '/vagrant/lab3/votes_re_bills.csv' WITH
(FORMAT csv, HEADER true, DELIMITER ',');
COPY votes_re_nominations FROM '/vagrant/lab3/votes_re_nominations.csv' WITH
(FORMAT csv, HEADER true, DELIMITER ',');


-- after data is loaded, add key and foreign key constraints and corresponding indexes

alter table only business
    add constraint bus_id primary key (id);

alter table only users
    add constraint bills_session_type_number_key unique (session, type, number);

alter table only users
    add constraint user_id primary key (id);

alter table only persons
    add constraint persons_id_govtrack_key unique (id_govtrack);

alter table only persons
    add constraint persons_id_lis_key unique (id_lis);

alter table only persons
    add constraint persons_pkey primary key (id);

alter table only states
    add constraint states_pkey primary key (id);

alter table only votes
    add constraint votes_chamber_session_number_key unique (chamber, session, number);

alter table only votes
    add constraint votes_pkey primary key (id);

alter table only votes_re_amendments
    add constraint votes_re_amendments_pkey primary key (vote_id);

alter table only votes_re_bills
    add constraint votes_re_bills_pkey primary key (vote_id);

alter table only votes_re_nominations
    add constraint votes_re_nominations_pkey primary key (vote_id);

alter table only person_roles
    add constraint person_roles_person_id_fkey foreign key (person_id) references persons(id);

alter table only person_roles
    add constraint person_roles_state_fkey foreign key (state) references states(id);

alter table only person_votes
    add constraint person_votes_person_id_fkey foreign key (person_id) references persons(id);

alter table only person_votes
    add constraint person_votes_vote_id_fkey foreign key (vote_id) references votes(id);

alter table only votes_re_amendments
    add constraint votes_re_amendments_vote_id_fkey foreign key (vote_id) references votes(id);

alter table only votes_re_bills
    add constraint votes_re_bills_bill_id_fkey foreign key (bill_id) references bills(id);

alter table only votes_re_bills
    add constraint votes_re_bills_vote_id_fkey foreign key (vote_id) references votes(id);

alter table only votes_re_nominations
    add constraint votes_re_nominations_vote_id_fkey foreign key (vote_id) references votes(id);

