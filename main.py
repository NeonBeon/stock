#!/usr/bin/env python3
"""
Grow a Garden Discord Stock Notifier
Fetches stock data and sends Discord webhook notifications every 5 minutes
"""

import sys
import time
import traceback
from datetime import datetime
from discord_notifier import GardenStockNotifier

def wait_for_next_interval():
    """Wait until the next 5-minute interval (XX:05, XX:10, etc.) + 30 seconds"""
    now = datetime.now()
    current_minute = now.minute
    
    # Calculate next 5-minute interval
    next_interval = ((current_minute // 5) + 1) * 5
    if next_interval >= 60:
        next_interval = 0
        target_time = now.replace(hour=(now.hour + 1) % 24, minute=0, second=30, microsecond=0)
    else:
        target_time = now.replace(minute=next_interval, second=30, microsecond=0)
    
    # If we're past the target time for this hour, move to next interval
    if target_time <= now:
        next_interval = ((current_minute // 5) + 1) * 5
        if next_interval >= 60:
            next_interval = 0
            target_time = now.replace(hour=(now.hour + 1) % 24, minute=0, second=30, microsecond=0)
        else:
            target_time = now.replace(minute=next_interval, second=30, microsecond=0)
    
    wait_seconds = (target_time - now).total_seconds()
    print(f"⏰ Next check at {target_time.strftime('%H:%M:%S')} (waiting {wait_seconds:.0f} seconds)")
    time.sleep(wait_seconds)

def main():
    """Main entry point for the application"""
    try:
        print("🌱 Grow a Garden Stock Notifier Starting...")
        print("🔄 Running continuously - checking every 5 minutes at XX:05, XX:10, etc.")
        print("⚠️ Press Ctrl+C to stop")
        print("🚀 Running in persistent mode to prevent timeout")
        
        # Create notifier instance
        notifier = GardenStockNotifier()
        
        while True:
            try:
                # Wait for the next 5-minute interval + 30 seconds
                wait_for_next_interval()
                
                print(f"\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Checking for stock updates...")
                
                # Fetch and send stock update
                success = notifier.fetch_and_notify()
                
                if success:
                    print("✅ Stock notification sent successfully!")
                else:
                    print("❌ Failed to send stock notification - will retry at next interval")
                
                # Flush output to prevent buffering issues
                sys.stdout.flush()
                
            except Exception as e:
                print(f"💥 Error during stock check: {str(e)}")
                print("🔄 Will retry at next interval...")
                traceback.print_exc()
                sys.stdout.flush()
                
    except KeyboardInterrupt:
        print("\n⚠️ Stock notifier stopped by user")
        return 0
    except Exception as e:
        print(f"💥 Unexpected error: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
