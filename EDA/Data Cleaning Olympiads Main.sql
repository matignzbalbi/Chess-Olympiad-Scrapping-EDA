USE Olympiads
GO

SELECT * 
FROM MainTable

--- Remove Duplicates ---

WITH RowNumberCTE AS (
	SELECT *,
		ROW_NUMBER() OVER (
		PARTITION BY 
		white_pieces,
		black_pieces
		ORDER BY
			white_pieces
		) row_num
FROM MainTable
)
SELECT *
FROM RowNumberCTE
WHERE row_num > 1

WITH RowNumberCTE AS (
	SELECT *,
		ROW_NUMBER() OVER (
		PARTITION BY 
		white_pieces,
		black_pieces
		ORDER BY
			white_pieces
		) row_num
FROM MainTable
)
DELETE 
FROM RowNumberCTE
WHERE row_num > 1

/* UPPER Country Codes */ 

UPDATE MainTable
SET country_white = UPPER(country_white)

UPDATE MainTable
SET country_black = UPPER(country_black)

/* Add Country Names */

ALTER TABLE MainTable
ADD country_name_white nvarchar(MAX)

ALTER TABLE MainTable
ADD country_name_black nvarchar(MAX)

UPDATE MT
SET MT.country_name_white = C.country_name
FROM MainTable MT
JOIN Countries C
	ON MT.country_white = C.country_code

UPDATE MT
SET MT.country_name_black = C.country_name
FROM MainTable MT
JOIN Countries C
	ON MT.country_black = C.country_code

ALTER TABLE MainTable
ALTER COLUMN accuracy_white FLOAT

ALTER TABLE MainTable
ALTER COLUMN accuracy_black FLOAT

SELECT opening
FROM MainTable
WHERE opening LIKE '%Sicilian%'


/* Cleaning results */

BEGIN TRANSACTION

UPDATE MainTable
SET game_result = CASE
		WHEN game_result LIKE '%' + LEFT(white_pieces, CHARINDEX(' ', white_pieces)) + '%' THEN 'White'
		WHEN game_result LIKE '%' + LEFT(black_pieces, CHARINDEX(' ', black_pieces)) + '%' THEN 'Black'
		WHEN game_result LIKE 'Tablas' THEN 'Draw'
		ELSE game_result
		END 

COMMIT

/* Fixing NULL Country Names */ 

SELECT DISTINCT
country_white,
country_name_white
FROM MainTable
WHERE country_name_white IS NULL


/* White */

BEGIN TRANSACTION

UPDATE MainTable
SET country_name_white = CASE
    WHEN country_white = 'AG' THEN 'Antigua and Barbuda'
    WHEN country_white = 'BN' THEN 'Brunei'
    WHEN country_white = 'BT' THEN 'Bhutan'
    WHEN country_white = 'CD' THEN 'Democratic Republic of the Congo'
    WHEN country_white = 'CI' THEN 'Ivory Coast'
    WHEN country_white = 'DM' THEN 'Dominica'
    WHEN country_white = 'GD' THEN 'Grenada'
    WHEN country_white = 'GG' THEN 'Guernsey'
    WHEN country_white = 'GQ' THEN 'Equatorial Guinea'
    WHEN country_white = 'GU' THEN 'Guam'
    WHEN country_white = 'GY' THEN 'Guyana'
    WHEN country_white = 'JE' THEN 'Jersey'
    WHEN country_white = 'KH' THEN 'Cambodia'
    WHEN country_white = 'KM' THEN 'Comoros'
    WHEN country_white = 'KW' THEN 'Kuwait'
    WHEN country_white = 'LA' THEN 'Laos'
    WHEN country_white = 'LC' THEN 'Saint Lucia'
    WHEN country_white = 'LR' THEN 'Liberia'
    WHEN country_white = 'LS' THEN 'Lesotho'
    WHEN country_white = 'MO' THEN 'Macau'
    WHEN country_white = 'MW' THEN 'Malawi'
    WHEN country_white = 'NA' THEN 'Namibia'
    WHEN country_white = 'SD' THEN 'Sudan'
    WHEN country_white = 'SL' THEN 'Sierra Leone'
    WHEN country_white = 'SN' THEN 'Senegal'
    WHEN country_white = 'SZ' THEN 'Eswatini'
    WHEN country_white = 'VG' THEN 'British Virgin Islands'
    WHEN country_white = 'XT' THEN 'Undefined Territory'
    ELSE country_name_white
END
WHERE country_name_white IS NULL;

COMMIT


/* Black */

SELECT DISTINCT
country_black,
country_name_black
FROM MainTable
WHERE country_name_black IS NULL

SELECT * 
FROM MainTable

BEGIN TRANSACTION

UPDATE MainTable
SET country_name_black = CASE country_black
    WHEN 'AG' THEN 'Antigua and Barbuda'
    WHEN 'BN' THEN 'Brunei'
    WHEN 'BT' THEN 'Bhutan'
    WHEN 'CD' THEN 'Democratic Republic of the Congo'
    WHEN 'CI' THEN 'Ivory Coast'
    WHEN 'DM' THEN 'Dominica'
    WHEN 'GD' THEN 'Grenada'
    WHEN 'GG' THEN 'Guernsey'
    WHEN 'GQ' THEN 'Equatorial Guinea'
    WHEN 'GU' THEN 'Guam'
    WHEN 'GY' THEN 'Guyana'
    WHEN 'JE' THEN 'Jersey'
    WHEN 'KH' THEN 'Cambodia'
    WHEN 'KM' THEN 'Comoros'
    WHEN 'KW' THEN 'Kuwait'
    WHEN 'LA' THEN 'Laos'
    WHEN 'LC' THEN 'Saint Lucia'
    WHEN 'LR' THEN 'Liberia'
    WHEN 'LS' THEN 'Lesotho'
    WHEN 'MO' THEN 'Macau'
    WHEN 'MW' THEN 'Malawi'
    WHEN 'NA' THEN 'Namibia'
    WHEN 'SD' THEN 'Sudan'
    WHEN 'SL' THEN 'Sierra Leone'
    WHEN 'SN' THEN 'Senegal'
    WHEN 'SZ' THEN 'Eswatini'
    WHEN 'VG' THEN 'British Virgin Islands'
    WHEN 'XT' THEN 'Undefined Territory'
    ELSE country_name_black
END
WHERE country_name_black IS NULL;

ROLLBACK