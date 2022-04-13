/*
 Here we have country_vaccination_stats table with columns 'country','date',
 'daily_vaccinations' and 'vaccines'.
 For all of the unique country values we are creating a median table of daily_vaccinations.
 Then we are checking each median value to see if a country has a daily_vaccinations median or not.
 If not we are assigning 0.
 */

SELECT country,
       CASE
           WHEN median_of_daily_vaccianations IS NULL THEN 0
           ELSE median_of_daily_vaccianations
           END as median
FROM (
         SELECT country, median(daily_vaccinations) as median_of_daily_vaccianations
         FROM country_vaccination_stats
         GROUP BY country
     ) as medianaded