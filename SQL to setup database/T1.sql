CREATE TRIGGER update_review_count_after_new_review ON review
AFTER INSERT AS
BEGIN
	UPDATE b
	-- Update the review count by simply counting the review again, following the requirements
	SET b.review_count = (
		SELECT COUNT(DISTINCT r.user_id)
		FROM review r
		WHERE r.business_id = b.business_id
	)
	FROM business b
		JOIN inserted i ON i.business_id = b.business_id;
END;