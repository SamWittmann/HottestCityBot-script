# HottestCityBot-script
A Twitter bot designed to run on AWS lambda that settles the age-old dispute of who's weather is hotter, every day.

Calculates which of the top 1,000 cities by population in the U.S. has the highest heat index each afternoon, and tweets the result [@hottest_city](https://twitter.com/hottest_city).

Very similar to [my previous Twitter bot for posting the hottest city](https://github.com/SamWittmann/hottestCityBot), just crammed into one (far more concise) Python file and designed to run on AWS lambda.

## APIs and external libraries used
* [OpenWeatherMap API](https://openweathermap.org/api) for fetching real-time weather data. 
* [meteocalc](https://github.com/malexer/meteocalc) for calculating heat indexes. 
* [requests-oauthlib](https://github.com/requests/requests-oauthlib) for... OAuth requests!
