import logging
import time
import requests
from typing import Dict, Any, Optional, List
import ccxt
from src.config.global_config import global_config

class BitgetClientWrapper:
    """Wrapper for Bitget client with error handling (supports both Spot and Futures)"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = None
        self.is_futures = global_config.BINANCE_FUTURES  # Keep same config name for compatibility
        self._last_request_time = 0
        self._min_request_interval = 1.0  # Minimum 1000ms between requests
        self._request_count = 0
        self._request_window_start = time.time()
        self._max_requests_per_minute = 500  # Conservative limit
        self._initialize_client()

    def _initialize_client(self):
        """Initialize Bitget client for Spot or Futures"""
        try:
            if global_config.BINANCE_TESTNET:  # Use same config name for testnet
                # Bitget sandbox environment
                self.client = ccxt.bitget({
                    'apiKey': global_config.BINANCE_API_KEY,  # Keep same config names
                    'secret': global_config.BINANCE_SECRET_KEY,
                    'password': global_config.BITGET_PASSPHRASE,  # New config needed
                    'sandbox': True,
                    'enableRateLimit': True,
                })
                self.logger.info("Bitget sandbox client initialized successfully")
            else:
                # Bitget production environment
                self.client = ccxt.bitget({
                    'apiKey': global_config.BINANCE_API_KEY,
                    'secret': global_config.BINANCE_SECRET_KEY,
                    'password': global_config.BITGET_PASSPHRASE,
                    'sandbox': False,
                    'enableRateLimit': True,
                })
                mode = "FUTURES" if self.is_futures else "SPOT"
                self.logger.info(f"Bitget {mode} production client initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize Bitget client: {e}")
            raise

    def _rate_limit(self):
        """Enhanced rate limiting with sliding window to prevent IP bans"""
        current_time = time.time()

        # Reset request count every minute
        if current_time - self._request_window_start > 60:
            self._request_count = 0
            self._request_window_start = current_time

        # Check if we're approaching rate limits
        if self._request_count >= self._max_requests_per_minute:
            sleep_time = 60 - (current_time - self._request_window_start)
            if sleep_time > 0:
                self.logger.warning(f"Rate limit protection: sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
                self._request_count = 0
                self._request_window_start = time.time()

        # Minimum interval between requests
        time_since_last = current_time - self._last_request_time
        if time_since_last < self._min_request_interval:
            time.sleep(self._min_request_interval - time_since_last)

        self._last_request_time = time.time()
        self._request_count += 1

    async def test_connection(self) -> bool:
        """Test API connection with improved error handling"""
        try:
            self._rate_limit()
            # Test connection
            markets = self.client.load_markets()

            env = "SANDBOX" if global_config.BINANCE_TESTNET else "PRODUCTION"
            self.logger.info(f"✅ Connected to Bitget {env}")
            self.logger.info("✅ Bitget API connection test successful")
            return True

        except Exception as e:
            self.logger.error(f"❌ Bitget API connection test failed: {e}")
