SELECT
    COUNT(DISTINCT PA_OF_INNING) AS total_two_strike_PAs, -- Total plate appearances with two strikes and no strikeout 
    SUM(CASE
        WHEN (BALLS = 0 AND STRIKES = 2) THEN 1
        ELSE 0
    END) AS count_through_0_2, -- Count of plate appearances passing through a 0-2 count 
    SUM(CASE
        WHEN (BALLS = 1 AND STRIKES = 2) THEN 1
        ELSE 0
    END) AS count_through_1_2, -- Count of plate appearances passing through a 1-2 count 
    SUM(CASE
        WHEN (BALLS = 2 AND STRIKES = 2) THEN 1
        ELSE 0
    END) AS count_through_2_2 -- Count of plate appearances passing through a 2-2 count
FROM 
    PITCHBYPITCH
WHERE
    PitcherName = 'Jackson, Luke' -- Filter for Luke Jackson
    AND STRIKES = 2 -- Focus on two-strike counts
    AND IS_STRIKEOUT = 0; -- Exclude plate appearances resulting in a strikeout