-- displays the businesses for the selected state, city, zipcode, and category
select b.name, b.address, b.city, b.stars, b.review_count, b.reviewrating, b.num_checkins 
from business as b, categories as c
where b.business_id = c.business_id AND b.state = 'AZ' AND b.city = 'Chandler' AND b.zipcode = '85248' AND c.category_name = 'Ice Cream & Frozen Yogurt'

-- popular business
select name, stars, reviewRating, review_count
from business 
where zipcode = '85248' AND stars > 
	(select avg(stars)
	from business
	 where zipcode = '85248'
	)
	AND review_count >
	(select avg(review_count)
	from business
	 where zipcode = '85248'
	)
ORDER BY Stars desc

-- successful
select name, stars, reviewRating, review_count
from business 
where zipcode = '85248' AND stars > 
	(select avg(stars)
	from business
	where zipcode = '85248'
	)
ORDER BY Stars desc

-- number of businesses in a zipcode
select count(*)
from business
where zipcode = '85248'

-- total population
select population
from zipcodeData
where zipcode = '85248'

-- average income
select meanIncome
from zipcodeData
where zipcode = '85248'