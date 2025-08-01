
#!/usr/bin/env python3
"""
Direct Telegram Message Content Test
===================================

This test directly inspects the actual message content generated by
the TelegramReporter for each type of notification, without relying
on complex mocking or patching mechanisms.
"""

import sys
import os
import json
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.reporting.telegram_reporter import TelegramReporter
from src.config.global_config import global_config

class DirectTelegramMessageTest:
    """Test Telegram message content directly"""
    
    def __init__(self):
        self.telegram_reporter = TelegramReporter()
        self.captured_messages = []
        
    def capture_message(self, original_method):
        """Capture the actual message content"""
        def wrapper(message):
            print(f"📱 CAPTURED MESSAGE CONTENT:")
            print("=" * 80)
            print(message)
            print("=" * 80)
            
            self.captured_messages.append({
                'timestamp': datetime.now().isoformat(),
                'method': original_method.__name__,
                'content': message,
                'length': len(message)
            })
            
            # If configured, try to send, otherwise just return True
            if self.telegram_reporter.enabled:
                try:
                    return original_method(message)
                except Exception as e:
                    print(f"❌ Send failed: {e}")
                    return False
            else:
                print("✅ Message captured (sending disabled)")
                return True
                
        return wrapper
    
    def test_all_message_types(self):
        """Test all Telegram message types and show their content"""
        print("🔍 DIRECT TELEGRAM MESSAGE CONTENT TEST")
        print("=" * 80)
        
        # Replace the send_message method to capture content
        original_send = self.telegram_reporter.send_message
        self.telegram_reporter.send_message = self.capture_message(original_send)
        
        try:
            # Test 1: Bot Startup
            print("\n🚀 TEST: Bot Startup Message")
            print("-" * 50)
            self.telegram_reporter.report_bot_startup(
                pairs=['BTCUSDT', 'ETHUSDT', 'SOLUSDT'],
                strategies=['rsi_oversold', 'macd_divergence', 'engulfing_pattern'],
                balance=1000.0,
                open_trades=0
            )
            
            # Test 2: Position Opened
            print("\n📈 TEST: Position Opened Message")
            print("-" * 50)
            position_data = {
                'strategy_name': 'RSI_OVERSOLD_SOLUSDT',
                'symbol': 'SOLUSDT',
                'side': 'BUY',
                'entry_price': 120.5500,
                'quantity': 0.83,
                'leverage': 5
            }
            self.telegram_reporter.report_position_opened(position_data)
            
            # Test 3: Position Closed
            print("\n📉 TEST: Position Closed Message")
            print("-" * 50)
            self.telegram_reporter.report_position_closed(
                position_data=position_data,
                exit_reason='Take Profit (RSI 70+)',
                pnl=3.88
            )
            
            # Test 4: Error Message
            print("\n❌ TEST: Error Message")
            print("-" * 50)
            self.telegram_reporter.report_error(
                error_type='API Connection Error',
                error_message='Failed to connect to Binance API after 3 retries',
                strategy_name='RSI_OVERSOLD_SOLUSDT'
            )
            
            # Test 5: Balance Warning
            print("\n💰 TEST: Balance Warning Message")
            print("-" * 50)
            self.telegram_reporter.report_balance_warning(
                required_balance=500.0,
                current_balance=125.50
            )
            
            # Test 6: Orphan Trade Detection
            print("\n👻 TEST: Orphan Trade Detection Message")
            print("-" * 50)
            self.telegram_reporter.report_orphan_trade_detected(
                strategy_name='RSI_OVERSOLD_SOLUSDT',
                symbol='SOLUSDT',
                side='BUY',
                entry_price=120.55
            )
            
            # Test 7: Bot Shutdown
            print("\n🛑 TEST: Bot Shutdown Message")
            print("-" * 50)
            self.telegram_reporter.report_bot_stopped(reason="Manual shutdown for testing")
            
        finally:
            # Restore original method
            self.telegram_reporter.send_message = original_send
        
        # Generate summary
        self.generate_summary()
        
    def generate_summary(self):
        """Generate and save test summary"""
        print(f"\n📊 MESSAGE CONTENT SUMMARY")
        print("=" * 80)
        print(f"📱 Total Messages Captured: {len(self.captured_messages)}")
        print(f"🔧 Telegram Configured: {'Yes' if self.telegram_reporter.enabled else 'No'}")
        
        for i, msg in enumerate(self.captured_messages, 1):
            print(f"\n{i}. {msg['method']} ({msg['length']} characters)")
            print(f"   Content: {msg['content'][:100]}...")
        
        # Save to file
        filename = f"telegram_message_content_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.captured_messages, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Full message content saved to: {filename}")
        except Exception as e:
            print(f"❌ Failed to save results: {e}")

def main():
    """Run the direct message content test"""
    tester = DirectTelegramMessageTest()
    tester.test_all_message_types()

if __name__ == "__main__":
    main()
