import requests
from config.settings import SOLANA_TRACKER_API_KEY, SOLANA_TRACKER_BASE_URL, API_FETCH_LIMIT
import time

async def get_first_token_buyers(token_mint_address: str) -> list | None:
    """
    Retrieves the first 100 buyers of a specific token with PnL data.
    Uses Solana Tracker API's /first-buyers/{token} endpoint.
    Args:
        token_mint_address (str): The mint address of the token.
    Returns:
        list | None: A list of buyer dictionaries if successful, None otherwise.
    """
    if not SOLANA_TRACKER_API_KEY:
        print("Solana Tracker API Key not found. Please set SOLANA_TRACKER_API_KEY in your.env file.")
        return None

    endpoint = f"{SOLANA_TRACKER_BASE_URL}/first-buyers/{token_mint_address}"
    headers = {"x-api-key": SOLANA_TRACKER_API_KEY}

    try:
        print(f"Fetching first buyers for token: {token_mint_address}...")
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()

        if data and isinstance(data, list):
            print(f"Successfully fetched {len(data)} first buyers.")
            return data
        else:
            print(f"No data or unexpected format received for first buyers of {token_mint_address}: {data}")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while fetching first buyers: {http_err} - Response: {response.text}")
        # Implement exponential backoff for rate limits if needed [2]
        return None
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred while fetching first buyers: {conn_err}")
        return None
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred while fetching first buyers: {timeout_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred while fetching first buyers: {req_err}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

async def get_wallet_pnl(wallet_address: str, token_mint_address: str = None) -> dict | None:
    """
    Retrieves Profit and Loss (PnL) data for a specific wallet, optionally for a specific token.
    Uses Solana Tracker API's /pnl/{wallet} or /pnl/{wallet}/{token} endpoint.
    Args:
        wallet_address (str): The public key of the wallet.
        token_mint_address (str, optional): The mint address of a specific token. If None, gets overall wallet PnL.
    Returns:
        dict | None: PnL data if successful, None otherwise.
    """
    if not SOLANA_TRACKER_API_KEY:
        print("Solana Tracker API Key not found. Please set SOLANA_TRACKER_API_KEY in your.env file.")
        return None

    if token_mint_address:
        endpoint = f"{SOLANA_TRACKER_BASE_URL}/pnl/{wallet_address}/{token_mint_address}"
    else:
        endpoint = f"{SOLANA_TRACKER_BASE_URL}/pnl/{wallet_address}"

    headers = {"x-api-key": SOLANA_TRACKER_API_KEY}

    try:
        print(f"Fetching PnL for wallet: {wallet_address}" + (f" for token: {token_mint_address}" if token_mint_address else "") + "...")
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data:
            print(f"Successfully fetched PnL data for {wallet_address}.")
            return data
        else:
            print(f"No PnL data found for {wallet_address}" + (f" for token {token_mint_address}" if token_mint_address else "") + ".")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while fetching PnL: {http_err} - Response: {response.text}")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred while fetching PnL: {conn_err}")
        return None
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred while fetching PnL: {timeout_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred while fetching PnL: {req_err}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

async def get_token_metadata(token_mint_address: str) -> dict | None:
    """
    Retrieves metadata for a specific token.
    Uses Solana Tracker API's /tokens/{tokenAddress} endpoint.
    Args:
        token_mint_address (str): The mint address of the token.
    Returns:
        dict | None: Token metadata if successful, None otherwise.
    """
    if not SOLANA_TRACKER_API_KEY:
        print("Solana Tracker API Key not found. Please set SOLANA_TRACKER_API_KEY in your.env file.")
        return None

    endpoint = f"{SOLANA_TRACKER_BASE_URL}/tokens/{token_mint_address}"
    headers = {"x-api-key": SOLANA_TRACKER_API_KEY}

    try:
        print(f"Fetching token metadata for: {token_mint_address}...")
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data and data.get('status') == 'success' and data.get('data'):
            print(f"Successfully fetched metadata for token: {token_mint_address}.")
            return data['data']
        else:
            print(f"No metadata or unexpected format received for token {token_mint_address}: {data}")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while fetching token metadata: {http_err} - Response: {response.text}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred while fetching token metadata: {req_err}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None