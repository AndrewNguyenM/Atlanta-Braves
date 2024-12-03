SELECT
    name, -- name 
    CASE 
        WHEN CAST(WAR AS REAL) >= 1 THEN 1 -- Check if WAR is at least 1
        ELSE 0
    END AS "1_plus_WAR", -- Indicator for achieving 1+ WAR 
    CASE
        WHEN CAST(WAR AS REAL) >= 2 THEN 1 -- Check if WAR is at least 2
        ELSE 0
    END AS "2_plus_WAR", -- Indicator for achieving 2+ WAR 
    CASE
        WHEN CAST(WAR AS REAL) >= 3 THEN 1 -- Check if WAR is at least 3
        ELSE 0
    END AS "3_plus_WAR", -- Indicator for achieving 3+ WAR
        CAST(WAR AS REAL) AS total_WAR -- Convert the WAR column to a numeric type and display as total yearly WAR 
FROM
    PERF -- Table 
WHERE
    Org = 'ATL' -- Filter for Team
    AND year = '2018' -- Filter for the 2018 season
    AND CAST(WAR AS REAL) > 0 -- Include only pitchers with at least one pitch (WAR > 0) 
ORDER BY
    total_WAR DESC; -- Sort the results by total yearly WAR in descending order