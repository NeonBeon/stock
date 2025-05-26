"""
Discord notification handler for Garden Stock updates
"""

import json
import requests
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from config import (
    SCRAPER_API_URL, DISCORD_WEBHOOK_URL, SEEDS, EGGS, GEAR,
    SEED_EMOJIS, EGG_EMOJIS, GEAR_EMOJIS, EMBED_COLOR, REQUEST_TIMEOUT, RARE_ITEMS
)

class GardenStockNotifier:
    """Handles fetching stock data and sending Discord notifications"""
    
    def __init__(self):
        """Initialize the notifier"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Garden-Stock-Notifier/1.0'
        })
        self.last_stock_data = None
    
    def fetch_stock_data(self) -> Optional[List[str]]:
        """
        Fetch stock data from the web scraper API
        
        Returns:
            List of span text elements or None if failed
        """
        try:
            print("📡 Fetching stock data from API...")
            
            response = self.session.get(SCRAPER_API_URL, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract span array from the response
            if 'result' not in data or 'span' not in data['result']:
                print("❌ Invalid API response structure")
                return None
                
            spans = data['result']['span']
            print(f"✅ Retrieved {len(spans)} span elements")
            
            return spans
            
        except requests.exceptions.Timeout:
            print("⏰ Request timed out while fetching stock data")
            return None
        except requests.exceptions.ConnectionError:
            print("🌐 Connection error while fetching stock data")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"🚫 HTTP error while fetching stock data: {e}")
            return None
        except json.JSONDecodeError:
            print("📄 Invalid JSON response from API")
            return None
        except Exception as e:
            print(f"💥 Unexpected error fetching stock data: {e}")
            return None
    
    def parse_stock_items(self, spans: List[str]) -> Dict[str, Dict[str, int]]:
        """
        Parse the span array to extract stock items and quantities
        
        Args:
            spans: List of span text elements
            
        Returns:
            Dictionary with categorized stock items and quantities
        """
        stock_data = {
            'seeds': {},
            'eggs': {},
            'gear': {}
        }
        
        print("🔍 Parsing stock items...")
        
        # Process spans in pairs (item name, quantity)
        i = 0
        while i < len(spans) - 1:
            item_name = spans[i].strip()
            quantity_text = spans[i + 1].strip()
            
            # Skip non-item elements
            if item_name in ["Cookie Policy", "&nbsp;VulcanValues", "|"] or not quantity_text.startswith('x'):
                i += 1
                continue
            
            # Extract quantity
            try:
                quantity = int(quantity_text[1:])  # Remove 'x' prefix
            except ValueError:
                i += 1
                continue
            
            # Categorize item
            if item_name in SEEDS:
                stock_data['seeds'][item_name] = quantity
                print(f"🌱 Found seed: {item_name} x{quantity}")
            elif item_name in EGGS:
                stock_data['eggs'][item_name] = quantity
                print(f"🥚 Found egg: {item_name} x{quantity}")
            elif item_name in GEAR:
                stock_data['gear'][item_name] = quantity
                print(f"⚙️ Found gear: {item_name} x{quantity}")
            
            i += 2  # Move to next item pair
        
        return stock_data
    
    def format_discord_message(self, stock_data: Dict[str, Dict[str, int]]) -> Dict:
        """
        Format the stock data into a Discord webhook message
        
        Args:
            stock_data: Categorized stock data
            
        Returns:
            Discord webhook payload
        """
        print("💬 Formatting Discord message...")
        
        # Check for rare items
        rare_items_found = []
        all_items = {}
        all_items.update(stock_data['seeds'])
        all_items.update(stock_data['eggs'])
        all_items.update(stock_data['gear'])
        
        for item in all_items:
            if item in RARE_ITEMS:
                rare_items_found.append(f"{item} (x{all_items[item]})")
        
        # Build the message content
        message_parts = ["**Garden Stock Update**\n"]
        
        # Add rare items alert if any found
        if rare_items_found:
            message_parts.append("🚨 **RARE ITEMS IN STOCK** 🚨")
            for rare_item in rare_items_found:
                message_parts.append(f"⭐ {rare_item}")
            message_parts.append("")  # Empty line
        
        # Seeds section
        if stock_data['seeds']:
            message_parts.append("🌱 **Seed Stock**")
            for item, quantity in sorted(stock_data['seeds'].items()):
                emoji = SEED_EMOJIS.get(item, "🌱")
                rare_indicator = " ⭐" if item in RARE_ITEMS else ""
                message_parts.append(f"{emoji} {item} - {quantity} units{rare_indicator}")
            message_parts.append("")  # Empty line
        
        # Eggs section
        if stock_data['eggs']:
            message_parts.append("🥚 **Egg Stock**")
            for item, quantity in sorted(stock_data['eggs'].items()):
                emoji = EGG_EMOJIS.get(item, "🥚")
                rare_indicator = " ⭐" if item in RARE_ITEMS else ""
                message_parts.append(f"{emoji} {item} - {quantity} units{rare_indicator}")
            message_parts.append("")  # Empty line
        
        # Gear section
        if stock_data['gear']:
            message_parts.append("⚙️ **Gear Stock**")
            for item, quantity in sorted(stock_data['gear'].items()):
                emoji = GEAR_EMOJIS.get(item, "⚙️")
                rare_indicator = " ⭐" if item in RARE_ITEMS else ""
                message_parts.append(f"{emoji} {item} - {quantity} units{rare_indicator}")
        
        # Create embed
        embed = {
            "title": "🌱 Garden Stock Update",
            "description": "\n".join(message_parts[1:]),  # Skip the title since it's in embed title
            "color": EMBED_COLOR,
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {
                "text": "Grow a Garden Stock Tracker"
            }
        }
        
        # Webhook payload - add ping if rare items found
        payload = {
            "embeds": [embed]
        }
        
        # Add @everyone ping if rare items are found
        if rare_items_found:
            payload["content"] = "@everyone 🚨 RARE ITEMS DETECTED! 🚨"
            print(f"🔔 Adding ping for rare items: {', '.join(rare_items_found)}")
        
        return payload
    
    def send_discord_webhook(self, payload: Dict) -> bool:
        """
        Send the formatted message to Discord webhook
        
        Args:
            payload: Discord webhook payload
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print("📤 Sending Discord webhook...")
            
            response = self.session.post(
                DISCORD_WEBHOOK_URL,
                json=payload,
                timeout=REQUEST_TIMEOUT,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            
            print("✅ Discord webhook sent successfully!")
            return True
            
        except requests.exceptions.Timeout:
            print("⏰ Request timed out while sending Discord webhook")
            return False
        except requests.exceptions.ConnectionError:
            print("🌐 Connection error while sending Discord webhook")
            return False
        except requests.exceptions.HTTPError as e:
            print(f"🚫 HTTP error while sending Discord webhook: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return False
        except Exception as e:
            print(f"💥 Unexpected error sending Discord webhook: {e}")
            return False
    
    def stock_data_changed(self, new_stock_data: Dict[str, Dict[str, int]]) -> bool:
        """
        Check if stock data has changed since last check
        
        Args:
            new_stock_data: Current stock data to compare
            
        Returns:
            True if data has changed, False otherwise
        """
        if self.last_stock_data is None:
            return True
        
        return new_stock_data != self.last_stock_data
    
    def fetch_and_notify(self) -> bool:
        """
        Complete workflow: fetch stock data and send Discord notification
        
        Returns:
            True if successful, False otherwise
        """
        # Fetch stock data
        spans = self.fetch_stock_data()
        if not spans:
            return False
        
        # Parse stock items
        stock_data = self.parse_stock_items(spans)
        
        # Check if we have any stock data
        total_items = sum(len(category) for category in stock_data.values())
        if total_items == 0:
            print("⚠️ No stock items found in the data")
            return False
        
        print(f"📊 Found {total_items} stock items total")
        
        # Check if stock data has changed
        if not self.stock_data_changed(stock_data):
            print("📋 Stock data unchanged - skipping notification")
            return True
        
        print("🆕 Stock data changed - sending update!")
        
        # Format Discord message
        payload = self.format_discord_message(stock_data)
        
        # Send to Discord
        success = self.send_discord_webhook(payload)
        
        # Update last stock data if successful
        if success:
            self.last_stock_data = stock_data.copy()
        
        return success
