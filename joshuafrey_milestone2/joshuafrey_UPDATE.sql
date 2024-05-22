UPDATE Business
SET num_checkins = C.sum 
FROM (
	SELECT business_id, sum(count)
	FROM CheckIn
	GROUP BY business_id
) as C
WHERE Business.business_id = C.business_id;

UPDATE Business
SET review_count = R.count
FROM (
	SELECT business_id, count(review_id)
	FROM review
	GROUP BY business_id) as R
WHERE Business.business_id = R.business_id;

UPDATE Business
SET reviewRating = (cast(R.sum as decimal) / R.count)
FROM (
	SELECT business_id, count(stars), sum(stars)
	FROM Review
	GROUP BY business_id) as R
WHERE Business.business_id = R.business_id;