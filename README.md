# HottestCityBot-script
A Twitter bot designed to run on AWS lambda that settles the age-old dispute of who's weather is hotter, every day.

Very similar to [my other Twitter bot for posting the hottest city](https://github.com/SamWittmann/hottestCityBot), just crammed into one Python file and designed to run on AWS lambda.

## APIs and external libraries used
[OpenWeatherMap API](https://openweathermap.org/api) for fetching real-time weather data.
[meteocalc](https://github.com/malexer/meteocalc) for calculating heat indexes.
[requests-oauthlib](https://github.com/requests/requests-oauthlib) for... OAuth requests!
