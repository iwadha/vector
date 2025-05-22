from api import solana_tracker
from db import supabase_manager
from config.settings import DEFAULT_DISCOVERY_TOKEN_MINT
import datetime

async def discover_and_store_wallets():
    """
    Discovers wallets by fetching first buyers of a default token
    and stores/updates them in the Supabase database.
    This function is designed for simplicity and a "small win".
    """
    print("\n--- Starting Wallet Discovery Process ---")

    # Step 1: Fetch first buyers for a predefined token
    # We use DEFAULT_DISCOVERY_TOKEN_MINT from settings.py (e.g., USDC)
    first_buyers_data = await solana_tracker.get_first_token_buyers(DEFAULT_DISCOVERY_TOKEN_MINT)

    if not first_buyers_data:
        print(f"No first buyers found for token {DEFAULT_DISCOVERY_TOKEN_MINT} or API call failed. Exiting discovery.")
        return

    print(f"Processing {len(first_buyers_data)} potential wallets...")

    # Step 2: Process each discovered wallet
    for buyer in first_buyers_data:
        wallet_address = buyer.get('wallet')
        if not wallet_address:
            print("Skipping buyer with no wallet address.")
            continue

        # Check if wallet already exists in our database
        existing_wallet = await supabase_manager.get_wallet(wallet_address)

        # Extract PnL data from the buyer response (Solana Tracker provides this directly)
        realized_pnl = buyer.get('realized', 0.0)
        unrealized_pnl = buyer.get('unrealized', 0.0)
        total_pnl = buyer.get('total', 0.0)

        # Simple heuristic for 'is_bot' for a "small win"
        # For now, we'll assume they are not bots unless we have strong indicators.
        # This can be refined later in wallet/analyzer.py
        is_bot = False 
        # Example: If a wallet has extremely high PnL but very few transactions, or
        # if 'first_buy_time' and 'last_transaction_time' are very close, it *might* be a bot.
        # For simplicity, we'll keep is_bot as False for now.

        wallet_data_to_store = {
            "wallet_address": wallet_address,
            "label": "First Buyer", # A simple label for now
            "is_bot": is_bot,
            # For initial score, we can use total PnL directly, or a simplified version
            "score": total_pnl, 
            "last_active": datetime.datetime.fromtimestamp(buyer.get('last_transaction_time', 0) / 1000, datetime.timezone.utc).isoformat() if buyer.get('last_transaction_time') else datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

        if existing_wallet:
            # Update existing wallet's score and last_active time
            print(f"Updating existing wallet: {wallet_address}")
            await supabase_manager.update_wallet(wallet_address, {
                "score": wallet_data_to_store["score"],
                "last_active": wallet_data_to_store["last_active"],
                "label": wallet_data_to_store["label"] # Update label if it changes
            })
        else:
            # Insert new wallet
            print(f"Inserting new wallet: {wallet_address}")
            await supabase_manager.insert_wallet(wallet_data_to_store)

        # Optionally, fetch token metadata and store it if not already present
        token_metadata = await solana_tracker.get_token_metadata(DEFAULT_DISCOVERY_TOKEN_MINT)
        if token_metadata:
            await supabase_manager.insert_token_metadata({
                "token_mint": token_metadata.get('mint'),
                "symbol": token_metadata.get('symbol'),
                "name": token_metadata.get('name'),
                "decimals": token_metadata.get('decimals'),
                "image_url": token_metadata.get('image'),
                "last_price_usd": token_metadata.get('priceUsd'),
                "last_price_updated": datetime.datetime.now(datetime.timezone.utc).isoformat()
            })

        # Add a small delay to respect API rate limits, even if not explicitly hit yet
        # For Solana Tracker free tier (10,000 requests/month, 1/second rate limit) [1]
        # A 1-second delay per wallet is a safe starting point.
        time.sleep(1) 

    print("\n--- Wallet Discovery Process Completed ---")