SELECT 
    DISTINCT name, -- Select the player's name
    SUM(CAST(WAR AS REAL)) AS combined_WAR, -- Calculate the combined WAR for 2002 and 2003
    MAX(CASE WHEN year = '2002' THEN CAST(WAR AS REAL) ELSE 0 END) AS WAR_2002, -- Maximum WAR for 2002
    MAX(CASE WHEN year = '2003' THEN CAST(WAR AS REAL) ELSE 0 END) AS WAR_2003 -- Maximum WAR for 2003
FROM 
    WAR -- Specify the table to query from
WHERE 
    year IN ('2002', '2003') -- Include only data from 2002 and 2003 
GROUP BY 
    name -- Group results by player name
HAVING
    MAX(CASE WHEN year = '2002' THEN CAST(WAR AS REAL) ELSE 0 END) > 3 -- Single-season WAR > 3 in 2002
    OR MAX(CASE WHEN year = '2003' THEN CAST(WAR AS REAL) ELSE 0 END) > 3 -- Single-season WAR > 3 in 2003
    OR SUM(CAST(WAR AS REAL)) > 5 -- Combined WAR > 5 for both years
ORDER BY 
    combined_WAR DESC; -- Sort results by combined WAR in descending order