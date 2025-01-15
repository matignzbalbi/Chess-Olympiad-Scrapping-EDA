USE Olympiads
GO

SELECT *
FROM MainTable

/* TOP 20 Openings most played*/ 

DROP TABLE IF EXISTS #Opening
CREATE TABLE #Opening (
opening nvarchar(MAX)
)

INSERT INTO #Opening (opening)
SELECT 
CASE
	WHEN opening LIKE '%:%' THEN SUBSTRING(opening, 1, CHARINDEX(':', opening, 1) - 1)
	ELSE opening
	END AS opening_formatted
FROM MainTable

SELECT TOP (20) opening,
COUNT(opening) AS total
FROM #Opening
GROUP BY opening
ORDER BY total DESC

/* Accuracy per country */ 

WITH AccuracyPerCountryCTE AS (
    SELECT 
        country,
        accuracy
    FROM (
        SELECT 
            country_name_white AS country, 
            accuracy_white AS accuracy 
        FROM MainTable
        UNION ALL
        SELECT 
            country_name_black AS country, 
            accuracy_black AS accuracy 
        FROM MainTable
    ) AS UnifiedData
    WHERE country IS NOT NULL AND LEN(LTRIM(RTRIM(country))) > 0
)
SELECT TOP 20 
    country,
    ROUND(AVG(accuracy), 2) AS AVG_Accuracy
FROM AccuracyPerCountryCTE
GROUP BY country
ORDER BY AVG_Accuracy DESC;


/* Accuracy Per Player */ 


WITH AccuracyPerPlayerCTE AS (
SELECT
	player,
	country,
	accuracy
	FROM (
		SELECT 
			white_pieces AS player,
			country_name_white AS country,
			accuracy_white AS accuracy
		FROM MainTable
		UNION ALL
		SELECT 
			black_pieces AS player,
			country_name_black AS country,
			accuracy_black AS accuracy
		FROM MainTable
	) AS DataPlayers
)
SELECT TOP 20
	player,
	country,
	ROUND(AVG(accuracy), 2) AS Accuracy,
	COUNT(*) AS GamesPlayed
FROM AccuracyPerPlayerCTE
GROUP BY player, country
HAVING COUNT(*) > 6
ORDER BY Accuracy DESC


DROP TABLE IF EXISTS #AccuracyXPlayer
CREATE TABLE #AccuracyXPlayer (
	player nvarchar(MAX),
	country nvarchar (MAX),
	accuracy float(5)
)

INSERT INTO #AccuracyXPlayer (player, country, accuracy)
SELECT 
	white_pieces,
	country_name_white,
	accuracy_white
FROM MainTable
UNION
SELECT black_pieces,
country_name_black,
accuracy_black
FROM MainTable

SELECT *
FROM #AccuracyXPlayer

/* 10 Games or MORE */ 

SELECT TOP 
	10 player,
	country,
	ROUND(AVG(accuracy), 2) AS AVG,
	COUNT(accuracy) AS games_played
FROM #AccuracyXPlayer
GROUP BY player, country
HAVING COUNT(*) >= 10
ORDER BY AVG DESC

/* No filter */ 

SELECT TOP 
	10 player,
	country,
	ROUND(AVG(accuracy), 2) AS AVG,
	COUNT(accuracy) AS games_played
FROM #AccuracyXPlayer
GROUP BY player, country
HAVING COUNT(*) >= 0
ORDER BY AVG DESC

/* Cleaning and checking results data */ 

WITH CTE AS(
	SELECT 
	white_pieces,
	black_pieces,
	game_result,
	CASE
		WHEN game_result LIKE '%' + LEFT(white_pieces, CHARINDEX(' ', white_pieces)) + '%' THEN 'White'
		WHEN game_result LIKE '%' + LEFT(black_pieces, CHARINDEX(' ', black_pieces)) + '%' THEN 'Black'
		WHEN game_result LIKE 'Tablas' THEN 'Draw'
		ELSE game_result
		END AS result
	FROM MainTable
)
SELECT result,
	COUNT(result) AS total,
	ROUND(
	(CAST(COUNT(result) AS FLOAT) / (SELECT COUNT(*) FROM CTE)) * 100, 2) as percentage
FROM CTE
GROUP BY result

SELECT *
FROM MainTable
WHERE game_result LIKE ''

DELETE FROM MainTable
WHERE game_result LIKE ''


/* Blunders per color */ 

WITH Blunders AS (
SELECT 
	black_blunders,
	COUNT(white_split.value) AS total_white
FROM MainTable
CROSS APPLY STRING_SPLIT(black_blunders, ',') AS white_split
GROUP BY black_blunders
)
SELECT 
	SUM(total_white) AS white_blunders
FROM Blunders

WITH WhiteBlunders AS (
    SELECT 
        white_pieces,
        COUNT(value) AS total_white_blunders
    FROM MainTable
    CROSS APPLY STRING_SPLIT(white_blunders, ',') AS white_split
    GROUP BY white_pieces
),
BlackBlunders AS (
    SELECT 
        black_pieces,
        COUNT(value) AS total_black_blunders
    FROM MainTable
    CROSS APPLY STRING_SPLIT(black_blunders, ',') AS black_split
    GROUP BY black_pieces
)
SELECT 
    COALESCE(SUM(wb.total_white_blunders), 0) AS total_white_blunders,
    COALESCE(SUM(bb.total_black_blunders), 0) AS total_black_blunders
FROM WhiteBlunders wb
FULL OUTER JOIN BlackBlunders bb
    ON wb.white_pieces = bb.black_pieces;

/* Accuracy per ELO */ 

DROP TABLE IF EXISTS #AccuracyXElo
CREATE TABLE #AccuracyXElo (
	elo float(10),
	accuracy float(10),
	bin nvarchar(10)
)

INSERT INTO #AccuracyXElo (elo, accuracy)
SELECT
	elo_white,
	accuracy_white
FROM MainTable
UNION 
SELECT
	elo_black,
	accuracy_black
FROM MainTable

SELECT
	MIN(elo) AS min,
	MAX(elo) AS max
FROM #AccuracyXElo


/* Percentiles */

SELECT DISTINCT 
	PERCENTILE_CONT(0.33) WITHIN GROUP (ORDER BY elo ASC) 
		OVER () AS Percentile33,
	PERCENTILE_CONT(0.66) WITHIN GROUP (ORDER BY elo ASC) 
		OVER () AS Percentile66
FROM #AccuracyXElo

WITH Percentiles AS (
	SELECT DISTINCT 
	PERCENTILE_CONT(0.33) WITHIN GROUP (ORDER BY elo ASC) 
		OVER () AS Percentile33,
	PERCENTILE_CONT(0.66) WITHIN GROUP (ORDER BY elo ASC) 
		OVER () AS Percentile66
FROM #AccuracyXElo
), 
Categorized AS (
SELECT
	elo,
	accuracy,
	CASE
		WHEN elo <= (SELECT Percentile33 FROM Percentiles) THEN 'Low Elo'
		WHEN elo <= (SELECT Percentile66 FROM Percentiles) THEN 'Medium Elo'
		ELSE 'High Elo'
		END AS Category
FROM #AccuracyXElo
) 
SELECT 
	ROUND(AVG(accuracy), 2) AS accuracy_avg,
	category
FROM Categorized
GROUP BY category
ORDER BY accuracy_avg DESC

--- Accuracy per Title ---

SELECT 
	title_white,
	ROUND(AVG(accuracy_white), 2) AS AVG_Accuracy,
	COUNT(*) AS countAll
FROM MainTable
GROUP BY title_white
HAVING COUNT(*) > 100
ORDER BY AVG_Accuracy DESC
