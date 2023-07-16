-- create stored procedure ComputeAverageScoreForUser
-- can be a decimal
DELIMITER $$
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
CREATE PROCEDURE ComputeAverageScoreForUser (`user_id` INTEGER)
BEGIN
	UPDATE users
	SET average_score = (SELECT AVG(score)
			    FROM corrections
			    WHERE corrections.user_id = users.id)
	WHERE id = user_id;
END $$
DELIMITER $$

