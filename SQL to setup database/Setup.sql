-- Drop the table in the reverse order of how we create it
IF OBJECT_ID('dbo.tip', 'U') IS NOT NULL
    DROP TABLE dbo.tip;

IF OBJECT_ID('dbo.review', 'U') IS NOT NULL
    DROP TABLE dbo.review;

IF OBJECT_ID('dbo.friendship', 'U') IS NOT NULL
    DROP TABLE dbo.friendship;

IF OBJECT_ID('dbo.user_yelp', 'U') IS NOT NULL
    DROP TABLE dbo.user_yelp;

IF OBJECT_ID('dbo.checkin', 'U') IS NOT NULL
    DROP TABLE dbo.checkin;

IF OBJECT_ID('dbo.business', 'U') IS NOT NULL
    DROP TABLE dbo.business;
	


-- Creating the tables
CREATE TABLE dbo.business (
    business_id CHAR(22) PRIMARY KEY,								-- Primary key, fixed-length string
    name VARCHAR(60) NOT NULL,										-- Variable-length string, can't be null
    address VARCHAR(75),											-- Optional variable-length string
    city VARCHAR(30) NOT NULL,										-- Variable-length string, can't be null
    postal_code VARCHAR(7),											-- Optional variable-length string
    stars DECIMAL(2, 1) CHECK (stars >= 1 AND stars <= 5),			-- Decimal with range [1,5]
    review_count INT DEFAULT 0 CHECK (review_count >= 0)			-- Integer with default 0 and non-negative constraint
);

CREATE TABLE dbo.checkin (
    checkin_id INT IDENTITY(1,1) PRIMARY KEY,						-- Primary key, auto-incrementing integer
    business_id CHAR(22) NOT NULL,									-- Foreign key referencing business.business_id
    date DATETIME NOT NULL DEFAULT GETDATE(),						-- Date field, defaults to current date and time
    FOREIGN KEY (business_id) REFERENCES dbo.business(business_id)	-- Foreign key constraint
);

CREATE TABLE dbo.user_yelp (
    user_id CHAR(22) PRIMARY KEY,									-- Primary key, fixed-length string
    name VARCHAR(35) NOT NULL,										-- Variable-length string, can't be null
    review_count INT DEFAULT 0 CHECK (review_count >= 0),			-- Integer with default 0, non-negative
    yelping_since DATETIME NOT NULL DEFAULT GETDATE(),				-- Date field, defaults to current date and time
    useful INT DEFAULT 0 CHECK (useful >= 0),						-- Integer with default 0, non-negative
    funny INT DEFAULT 0 CHECK (funny >= 0),							-- Integer with default 0, non-negative
    cool INT DEFAULT 0 CHECK (cool >= 0),							-- Integer with default 0, non-negative
    fans INT DEFAULT 0 CHECK (fans >= 0),							-- Integer with default 0, non-negative
    average_stars DECIMAL(3, 2) 
		CHECK (average_stars >= 1 AND average_stars <= 5)			-- Decimal with range [1,5]
);

CREATE TABLE dbo.friendship (
    user_id CHAR(22) NOT NULL,										-- Foreign key referencing user_yelp.user_id
    friend CHAR(22) NOT NULL,										-- Foreign key referencing user_yelp.user_id
    PRIMARY KEY (user_id, friend),									-- Composite primary key (user_id + friend)
    FOREIGN KEY (user_id) REFERENCES dbo.user_yelp(user_id),		-- Foreign key constraint on user_id
    FOREIGN KEY (friend) REFERENCES dbo.user_yelp(user_id)			-- Foreign key constraint on friend
);

CREATE TABLE dbo.review (
    review_id CHAR(22) PRIMARY KEY,									-- Primary key, fixed-length string
    user_id CHAR(22) NOT NULL,										-- Foreign key referencing user_yelp.user_id
    business_id CHAR(22) NOT NULL,									-- Foreign key referencing business.business_id
    stars INT NOT NULL CHECK (stars >= 1 AND stars <= 5),			-- Integer for star rating, in [1,5]
    useful INT DEFAULT 0 CHECK (useful >= 0),						-- Non-negative integer, default 0
    funny INT DEFAULT 0 CHECK (funny >= 0),							-- Non-negative integer, default 0
    cool INT DEFAULT 0 CHECK (cool >= 0),							-- Non-negative integer, default 0
    date DATETIME DEFAULT GETDATE(),								-- Date field, defaults to current date and time
    FOREIGN KEY (user_id) REFERENCES dbo.user_yelp(user_id),		-- Foreign key constraint on user_id
    FOREIGN KEY (business_id) REFERENCES dbo.business(business_id)	-- Foreign key constraint on business_id
);

CREATE TABLE dbo.tip (
    tip_id INT IDENTITY(1,1) PRIMARY KEY,							-- Primary key, auto-incrementing integer
    user_id CHAR(22) NOT NULL,										-- Foreign key referencing user_yelp.user_id
    business_id CHAR(22) NOT NULL,									-- Foreign key referencing business.business_id
    date DATETIME NOT NULL DEFAULT GETDATE(),						-- Date field, defaults to current date and time
    compliment_count INT DEFAULT 0 CHECK (compliment_count >= 0),	-- Non-negative integer, default 0
    FOREIGN KEY (user_id) REFERENCES dbo.user_yelp(user_id),		-- Foreign key constraint on user_id
    FOREIGN KEY (business_id) REFERENCES dbo.business(business_id)	-- Foreign key constraint on business_id
);



-- Inserting the sample data
BULK INSERT dbo.business
FROM 'd:\userdata\kzcheng354\a3dataset\business.csv'
WITH (
    FIELDTERMINATOR = ',',											-- Fields are separated by commas
    ROWTERMINATOR = '\n',											-- Rows are terminated by new lines
    FIRSTROW = 2													-- Skip the header row in the CSV file
);

BULK INSERT dbo.checkin
FROM 'd:\userdata\kzcheng354\a3dataset\checkin.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);

BULK INSERT dbo.user_yelp
FROM 'd:\userdata\kzcheng354\a3dataset\user_yelp.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);

BULK INSERT dbo.friendship
FROM 'd:\userdata\kzcheng354\a3dataset\friendship.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);

BULK INSERT dbo.review
FROM 'd:\userdata\kzcheng354\a3dataset\review.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);

BULK INSERT dbo.tip
FROM 'd:\userdata\kzcheng354\a3dataset\tip.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);
