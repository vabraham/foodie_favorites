# Foodie Favorites

Check out the live app: www.foodiefavorites.co

Foodie Favorites is a webapp created to help users make more informed decisions about what they eat when they go out to popular restaurants. It uses Natural Language Processing to classify food mentions in Yelp reviews and subsequently matches those mentions to menu items to help users find out what dishes are most popular.

![Image of Landing Page]
(images/2016-03-20_15-26-07_1.png)

## Inspiration
When going out to eat at a nice restaurant in the city, I frequently see people browsing their phones looking at Yelp reviews and pictures, frantically trying to make a decision about what to order before their waiter gets back to the table. Instead of wasting all that time, what if there was a service that would quickly and accurately tell you what is popular without having to fish for it yourself. So that's what I set out to do by creating Foodie Favorites.

## Data Sourcing
The Yelp data that I needed was a little tricky to get, while they have an easily accessible API, it's very limiting in what data it provides. I needed lots of reviews and restaurant menus, neither of which was readily available through the API. Yelp does provide some amazingly rich academic datasets as part of its Yelp Dataset Challenge. I used a slightly older one, which contained well over 200,000 reviews from 2006-2012 for restaurants in Chicago, Boston, Los Angeles, Washington D.C., Philadelphia, New York, and San Francisco. Since the data files are somewhat large (>100 mb), I have provided them in a [zip file](/data/Yelp_data_json_2006_2012.zip).  