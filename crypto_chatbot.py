import requests
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Create friendly chatbot
chatbot = ChatBot("CryptoBuddy")
trainer = ListTrainer(chatbot)

trainer.train([
    "Which crypto is trending?",
    "Hey there! 🚀 Right now, Bitcoin and Cardano are climbing the charts!",
    "Which crypto is sustainable?",
    "Easy choice! 🌱 Cardano is leading the way with low energy use.",
    "Which crypto is a good investment?",
    "Bitcoin and Ethereum are solid options, but keep an eye on Cardano!"
])

# Crypto database with personality
crypto_db = {  
    "Bitcoin": {"price_trend": "rising", "market_cap": "high", "energy_use": "high", "sustainability_score": 3},  
    "Ethereum": {"price_trend": "stable", "market_cap": "high", "energy_use": "medium", "sustainability_score": 6},  
    "Cardano": {"price_trend": "rising", "market_cap": "medium", "energy_use": "low", "sustainability_score": 8}  
}

# Fetch real-time crypto prices
def get_crypto_price(crypto_name):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_name}&vs_currencies=usd"
    response = requests.get(url).json()
    return response.get(crypto_name, {}).get("usd", "Data unavailable")

# Chatbot logic with engaging responses
def analyze_crypto(user_query):
    if "sustainable" in user_query:
        recommend = max(crypto_db.keys(), key=lambda x: crypto_db[x]["sustainability_score"])
        return f"🌱 You should check out {recommend}! It's one of the most energy-efficient cryptos."

    elif "trending" in user_query:
        trending_coins = [coin for coin, data in crypto_db.items() if data["price_trend"] == "rising"]
        return f"🚀 These cryptos are hot right now: {', '.join(trending_coins)}!"

    elif "profitable" in user_query:
        profitable_coins = [coin for coin, data in crypto_db.items() if data["price_trend"] == "rising" and data["market_cap"] == "high"]
        return f"💰 If you’re looking for strong investments, consider: {', '.join(profitable_coins)}."

    elif "price" in user_query:
        coin = user_query.split()[-1].lower()
        price = get_crypto_price(coin)
        return f"📈 {coin.capitalize()}'s current price is **${price}**!"

    else:
        return "🤔 I'm still learning! Try asking about trends, sustainability, or profitability."

# Personalized investment insights
def personalized_insights(risk_level, investment_goal, sustainability_preference):
    recommendations = []
    for coin, data in crypto_db.items():
        if risk_level == "high" and data["price_trend"] == "rising":
            recommendations.append(coin)
        elif risk_level == "medium" and data["market_cap"] in ["high", "medium"]:
            recommendations.append(coin)
        elif risk_level == "low" and data["market_cap"] == "high" and data["price_trend"] != "declining":
            recommendations.append(coin)

        if sustainability_preference == "yes" and data["sustainability_score"] > 6:
            recommendations.append(coin)

    if investment_goal == "short-term":
        recommendations = [coin for coin in recommendations if crypto_db[coin]["price_trend"] == "rising"]

    if not recommendations:
        return "Hmm... Based on your preferences, I suggest researching more options! 🔍"

    return f"📊 Based on your profile, consider investing in: {', '.join(set(recommendations))}!"
