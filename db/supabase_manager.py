from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_ANON_KEY
import datetime

# Global variable for the Supabase client
supabase: Client = None

def initialize_supabase_client():
    """
    Initializes the Supabase client using credentials from settings.
    This function should be called once at the application start.
    """
    global supabase
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        print("Error: Supabase URL or Anon Key not found in environment variables.")
        print("Please ensure SUPABASE_URL and SUPABASE_ANON_KEY are set in your.env file.")
        return None
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        print("Supabase client initialized successfully.")
        return supabase
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")
        return None

async def insert_wallet(wallet_data: dict) -> bool:
    """
    Inserts a new wallet record into the 'wallets' table.
    Args:
        wallet_data (dict): A dictionary containing wallet information.
                            Expected keys: 'wallet_address', 'label', 'score', 'is_bot'.
    Returns:
        bool: True if insertion is successful, False otherwise.
    """
    if not supabase:
        print("Supabase client not initialized. Call initialize_supabase_client() first.")
        return False
    try:
        # Ensure 'first_seen' and 'last_active' are set if not provided
        current_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
        if 'first_seen' not in wallet_data:
            wallet_data['first_seen'] = current_time
        if 'last_active' not in wallet_data:
            wallet_data['last_active'] = current_time
        if 'created_at' not in wallet_data:
            wallet_data['created_at'] = current_time
        if 'updated_at' not in wallet_data:
            wallet_data['updated_at'] = current_time

        response = await supabase.table("wallets").insert(wallet_data).execute()
        if response.data:
            print(f"Wallet {wallet_data.get('wallet_address', 'N/A')} inserted successfully.")
            return True
        else:
            # Supabase client might return an error object in 'error' field
            print(f"Failed to insert wallet {wallet_data.get('wallet_address', 'N/A')}: {response.error}")
            return False
    except Exception as e:
        print(f"Error inserting wallet {wallet_data.get('wallet_address', 'N/A')}: {e}")
        return False

async def get_wallet(wallet_address: str) -> dict | None:
    """
    Retrieves a wallet record from the 'wallets' table by its address.
    Args:
        wallet_address (str): The public key of the wallet.
    Returns:
        dict | None: The wallet data if found, None otherwise.
    """
    if not supabase:
        print("Supabase client not initialized. Call initialize_supabase_client() first.")
        return None
    try:
        response = await supabase.table("wallets").select("*").eq("wallet_address", wallet_address).limit(1).execute()
        if response.data:
            return response.data
        return None
    except Exception as e:
        print(f"Error retrieving wallet {wallet_address}: {e}")
        return None

async def update_wallet(wallet_address: str, update_data: dict) -> bool:
    """
    Updates an existing wallet record in the 'wallets' table.
    Args:
        wallet_address (str): The public key of the wallet to update.
        update_data (dict): A dictionary containing fields to update.
    Returns:
        bool: True if update is successful, False otherwise.
    """
    if not supabase:
        print("Supabase client not initialized. Call initialize_supabase_client() first.")
        return False
    try:
        # Always update 'updated_at' timestamp
        update_data['updated_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        response = await supabase.table("wallets").update(update_data).eq("wallet_address", wallet_address).execute()
        if response.data:
            print(f"Wallet {wallet_address} updated successfully.")
            return True
        else:
            print(f"Failed to update wallet {wallet_address}: {response.error}")
            return False
    except Exception as e:
        print(f"Error updating wallet {wallet_address}: {e}")
        return False

async def insert_token_metadata(token_data: dict) -> bool:
    """
    Inserts or updates token metadata in the 'token_metadata' table.
    Args:
        token_data (dict): Dictionary with token details.
    Returns:
        bool: True if successful, False otherwise.
    """
    if not supabase:
        print("Supabase client not initialized. Call initialize_supabase_client() first.")
        return False
    try:
        current_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
        token_data['updated_at'] = current_time
        if 'created_at' not in token_data:
            token_data['created_at'] = current_time

        # Use upsert to insert if not exists, update if exists
        response = await supabase.table("token_metadata").upsert(token_data, on_conflict="token_mint").execute()
        if response.data:
            print(f"Token metadata for {token_data.get('token_mint', 'N/A')} upserted successfully.")
            return True
        else:
            print(f"Failed to upsert token metadata {token_data.get('token_mint', 'N/A')}: {response.error}")
            return False
    except Exception as e:
        print(f"Error upserting token metadata {token_data.get('token_mint', 'N/A')}: {e}")
        return False