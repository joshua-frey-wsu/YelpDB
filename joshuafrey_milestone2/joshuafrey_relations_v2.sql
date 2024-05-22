CREATE TABLE Business (
	business_id VARCHAR(50),
	name VARCHAR(100),
	address VARCHAR(100),
	state VARCHAR(2),
	city VARCHAR(30),
	zipcode CHAR(5),
	longitude FLOAT,
	latitude FLOAT,
    stars FLOAT,
	reviewRating FLOAT,
	review_count INTEGER,
	open_status BOOLEAN,
	num_checkins INTEGER,
    PRIMARY KEY (business_id)
);

CREATE TABLE Review (
    review_id VARCHAR(50),
    user_id VARCHAR(50),
    business_id VARCHAR(50),
    stars INTEGER,
    date DATE,
    cool INTEGER,
	funny INTEGER,
	useful INTEGER,
    text VARCHAR(2500),
    Primary Key(review_id),
    FOREIGN KEY(business_id) REFERENCES Business(business_id)
);

CREATE TABLE CheckIn (
    business_id VARCHAR(50),
	day VARCHAR(10),
	count INTEGER,
	PRIMARY KEY(business_id, day),
	FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

CREATE TABLE Categories (
    category_name VARCHAR(50),
    business_id VARCHAR(50),
    Primary KEY(business_id, category_name),
    FOREIGN KEY(business_id) REFERENCES Business(business_id)
);
