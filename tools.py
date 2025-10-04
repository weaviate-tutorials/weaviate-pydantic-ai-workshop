import random


def get_weather_for_city(city: str) -> str:
    """Get weather for any city"""
    if city == "Edinburgh":
        rand_weather = random.choice(["cloudy", "rainy", "unusually sunny"])
        rand_temp = random.randint(5, 10)
    else:
        rand_weather = random.choice(["sunny", "cloudy", "rainy", "snowy"])
        rand_temp = random.randint(15, 20)

    return f"The weather in {city} is {rand_weather} today. The expected temperature is {rand_temp} degrees Celsius."


def get_trending_news_for_city(city: str) -> str:
    return f"""
    Today in {city}, a surprisingly large {random.choice(["mouse", "snake", "mongoose"])}
    was found {random.choice(["chasing", "cuddling", "playing"])}
    with a startled {random.choice(["child", "jogger", "park manager"])}.
    """
