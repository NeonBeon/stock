"""
Configuration settings for the Garden Stock Notifier
"""

import os

# API Endpoints
SCRAPER_API_URL = "https://web.scraper.workers.dev/?url=https%3A%2F%2Fvulcanvalues.com%2Fgrow-a-garden%2Fstock&selector=span&scrape=text&pretty=true"
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")  # Read from environment variable

# Item Categories
SEEDS = [
    "Carrot", "Strawberry", "Blueberry", "Orange Tulip", "Tomato", "Bamboo",
    "Watermelon", "Apple", "Pepper", "Mango", "Daffodil", "Pumpkin", "Corn",
    "Coconut", "Cactus", "Cacao", "Dragon Fruit", "Grape", "Mushroom", "Beanstalk"
]

EGGS = [
    "Common Egg", "Rare Egg", "Uncommon Egg", "Legendary Egg", "Bug Egg", "Mythical Egg"
]

GEAR = [
    "Watering Can", "Trowel", "Favorite Tool", "Basic Sprinkler", "Godly Sprinkler",
    "Advanced Sprinkler", "Master Sprinkler", "Lightning Rod", "Recall Wrench"
]

# Emoji mappings
SEED_EMOJIS = {
    "Carrot": "🥕",
    "Strawberry": "🍓",
    "Blueberry": "🫐",
    "Orange Tulip": "🌷",
    "Tomato": "🍅",
    "Bamboo": "🎋",
    "Watermelon": "🍉",
    "Apple": "🍎",
    "Pepper": "🌶️",
    "Mango": "🥭",
    "Daffodil": "🌼",
    "Pumpkin": "🎃",
    "Corn": "🌽",
    "Coconut": "🥥",
    "Cactus": "🌵",
    "Cacao": "🫘",
    "Dragon Fruit": "🐉",
    "Grape": "🍇",
    "Mushroom": "🍄",
    "Beanstalk": "🌱"
}

EGG_EMOJIS = {
    "Common Egg": "🥚",
    "Rare Egg": "🥚",
    "Uncommon Egg": "🥚",
    "Legendary Egg": "🥚",
    "Bug Egg": "🥚",
    "Mythical Egg": "🥚"
}

GEAR_EMOJIS = {
    "Watering Can": "🚿",
    "Trowel": "🛠️",
    "Favorite Tool": "❤️",
    "Basic Sprinkler": "💦",
    "Godly Sprinkler": "✨",
    "Advanced Sprinkler": "🌊",
    "Master Sprinkler": "💎",
    "Lightning Rod": "⚡",
    "Recall Wrench": "🔧"
}

# Discord embed color (green)
EMBED_COLOR = 0x00FF00

# Request timeout settings
REQUEST_TIMEOUT = 30

# Rare items that should trigger ping notifications
RARE_ITEMS = [
    "Beanstalk", "Mushroom", "Dragon Fruit", "Cacao", "Cactus", "Coconut", 
    "Mango", "Pepper", "Bamboo", "Mythical Egg", "Bug Egg", "Legendary Egg",
    "Lightning Rod", "Master Sprinkler", "Godly Sprinkler"
]
