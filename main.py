import asyncio
from db.supabase_manager import initialize_supabase_client
from wallet.discovery import discover_and_store_wallets

async def main():
    """
    Main function to initialize the application and start the wallet discovery process.
    """
    print("Starting Solana Copy Trading Bot Application...")

    # Initialize Supabase client
    supabase_client = initialize_supabase_client()
    if not supabase_client:
        print("Application cannot proceed without Supabase client. Exiting.")
        return

    # Start the wallet discovery process
    await discover_and_store_wallets()

    print("Application finished. You can now check your Supabase database.")

if __name__ == "__main__":
    # Run the asynchronous main function
    asyncio.run(main())