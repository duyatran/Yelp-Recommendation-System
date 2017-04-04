-- drop the tables if they already exist

--DROP TABLE IF EXISTS businesses CASCADE;
--DROP TABLE IF EXISTS business_hours CASCADE;
-- DROP TABLE IF EXISTS friends CASCADE;
--DROP TABLE IF EXISTS elite_users CASCADE;
--DROP TABLE IF EXISTS check_ins CASCADE;
--DROP TABLE IF EXISTS reviews CASCADE;
--DROP TABLE IF EXISTS tips CASCADE;
--DROP TABLE IF EXISTS users CASCADE;

-- create the tables and views
-- note: primary keys and foreign keys are specified at the end of this file
-- (indexes created after data is loaded)


-- business
CREATE TABLE businesses (
    bus_id character varying(100) PRIMARY KEY,
    bus_name character varying(200),
    neighborhood character varying(200),
    address character varying(200),
    city character varying(200),
    state character varying(15),
    postCode character varying(10),
    latitude double precision,
    longitude double precision,
    stars double precision,
    review_count integer,
    is_open boolean,
    attributes text[], -- an array of strings: each array element is an attribute
    categories text[] -- an array of strings of business categories
);

-- business hours
CREATE TABLE business_hours (
    bus_id character varying(100) REFERENCES "businesses",
    day integer NOT NULL,
    open_time time,
    close_time time
);


-- check-ins
CREATE TABLE check_ins (
  bus_id character varying(100) NOT NULL REFERENCES "businesses",
  day integer,
  hour integer,
  count integer
);



CREATE TABLE users (
    user_id character varying(100) NOT NULL PRIMARY KEY,
    name character varying(100) NOT NULL,
    review_count integer NOT NULL,
    yelp_since date NOT NULL, -- format like 2009-12-19
    friends text[], -- ideally, friendship would be a separate table, but populating that table takes too long
    useful integer, -- number of useful votes sent by the user
    funny integer, -- number of funny votes sent by the user
    cool integer, -- number of cool votes sent by the user
    fans integer, -- number of fans the user has
    avg_stars double precision,
    compliment_hot integer, -- number of hot compliments received by the user
    compliment_more integer, -- number of more compliments received by the user
    compliment_profile integer, -- number of profile compliments received by the user
    compliment_cute integer, -- number of cute compliments received by the user
    compliment_list integer, -- number of list compliments received by the user
    compliment_note integer, -- number of note compliments received by the user
    compliment_plain integer, -- number of plain compliments received by the user
    compliment_cool integer, -- number of cool compliments received by the user
    compliment_funny integer, -- number of funny compliments received by the user
    compliment_writer integer, -- number of writer compliments received by the user
    compliment_photos integer  -- number of photos compliments received by the user
);

-- CREATE TABLE friends (
--     user_id1 character varying(100) REFERENCES users (user_id),
--     user_id2 character varying(100)
-- );

CREATE TABLE elite_users (
    user_id character varying(100) REFERENCES users,
    year integer NOT NULL
);

CREATE TABLE reviews (
    review_id character varying(100) NOT NULL PRIMARY KEY,
    user_id character varying(100) NOT NULL REFERENCES users,
    bus_id character varying(100) NOT NULL REFERENCES businesses,
    stars double precision,
    review_date date,
    review_text text,
    useful integer, -- number of useful votes received
    funny integer, -- number of funny votes received
    cool integer -- number of cool votes received
);

CREATE TABLE tips (
  tip_text text,
  tip_date date, -- format like 2009-12-19
  likes int, -- like count
  bus_id character varying(100) REFERENCES businesses,
  user_id character varying(100) REFERENCES users
);