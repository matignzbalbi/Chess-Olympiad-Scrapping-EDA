USE Olympiads
GO

SELECT * 
FROM OlympiadsMain

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
FROM OlympiadsMain
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
FROM OlympiadsMain
)
DELETE 
FROM RowNumberCTE
WHERE row_num > 1

