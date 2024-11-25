CREATE TRIGGER prevent_reviewing_without_friend ON review
AFTER INSERT AS
BEGIN
	-- Check if there exists an inserted review that violates the condition
    IF EXISTS (
        SELECT *
        FROM inserted i
        WHERE NOT EXISTS (
			-- With the condition being, there exists a review on the same business which is left by a friend of the new reviewer.
            SELECT *
            FROM review r, friendship f
			WHERE r.business_id = i.business_id		-- Find all other reviews for this business
				AND ((
					i.user_id = f.user_id AND		-- In the friendship table, find the user to find the friend,
					f.friend = r.user_id			-- then check to see for each review, if this friend left that review
				) OR (
					i.user_id = f.friend AND		-- Also check the reverse case
					f.user_id = r.user_id
				))
        )
    )
	BEGIN
        -- If a violation is found, raise an error and rollback the transaction
		RAISERROR('You must have at least one friend who has reviewed this business.', 16, 1);
        ROLLBACK TRANSACTION;
	END
END;