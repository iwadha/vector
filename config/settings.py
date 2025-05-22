import os
from dotenv import load_dotenv

# Load environment variables from.env file
load_dotenv()

# --- Supabase Credentials ---
# These are loaded from your.env file
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# --- Solana Tracker API Key ---
# You will need to get this from the Solana Tracker website
SOLANA_TRACKER_API_KEY = os.getenv("SOLANA_TRACKER_API_KEY")

# --- API Endpoints ---
SOLANA_TRACKER_BASE_URL = "https://data.solanatracker.io"

# --- Configuration for Wallet Discovery ---
# Example token to find first buyers for. You can change this later.
# This is the mint address for a popular token (e.g., Wrapped SOL for testing, or a known memecoin)
# For a real project, you might want to dynamically get trending tokens first.
# For now, let's use a placeholder or a well-known token like USDC or SOL.
# Example: USDC mint address on Solana
DEFAULT_DISCOVERY_TOKEN_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v" # USDC
# Or for a memecoin, you'd find its mint address.

# --- General Application Settings ---
# Number of wallets to fetch in one API call (adjust based on API limits)
API_FETCH_LIMIT = 100