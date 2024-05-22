CREATE TABLE Business (
    business_id VARCHAR(20),
    state VARCHAR(2),
    city VARCHAR(30),
    zipcode INTEGER,
    name VARCHAR(50),
    stars INTEGER,
    address VARCHAR(100),
    review_count INTEGER,
    num_checkins INTEGER,
    reviewRating INTEGER,
    Primary Key(business_id)
);

CREATE TABLE Review (
    business_id VARCHAR(20),
    review_id VARCHAR(30),
    user_id VARCHAR(30),
    date DATE,
    stars INTEGER,
    text VARCHAR(2500),
    Primary Key(review_id),
    FOREIGN KEY(business_id) REFERENCES Business(business_id)
);

CREATE TABLE Check_In (
    business_id VARCHAR(20),
    day VARCHAR(15),
    time TIME,
    count INTEGER,
    Primary Key(business_id, day, time),
    FOREIGN KEY(business_id) REFERENCES Business(business_id)
);

CREATE TABLE Categories (
    business_id VARCHAR(20),
    category_name VARCHAR(20),
    Primary KEY(business_id, category_name),
    FOREIGN KEY(business_id) REFERENCES Business(business_id)
);

CREATE TABLE Attributes (
    business_id VARCHAR(20),
    attr_name VARCHAR(20),
    value INTEGER,
    Primary KEY(business_id, attr_name),
    FOREIGN KEY(business_id) REFERENCES Business(business_id)
);

