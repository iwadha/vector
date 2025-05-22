import requests
from config.settings import MORALIS_API_KEY, MORALIS_BASE_URL, MORALIS_V2_BASE_URL
import time
import asyncio # Needed for async functions

# Helper function for making Moralis API requests
async def _make_moralis_request(url: str, params: dict = None) -> dict | None:
    """
    Internal helper to make requests to Moralis API.
    Handles headers, basic error checking, and returns JSON data.
    """
    if not MORALIS_API_KEY:
        print("Moralis API Key not found. Please set MORALIS_API_KEY in your.env file.")
        return None

    headers = {
        "X-API-Key": MORALIS_API_KEY,
        "accept": "application/json"
    }

    try:
        # Using requests.get directly, but in an async context, it's better to use aiohttp
        # For simplicity and "small win", we'll stick to requests for now,
        # but be aware that requests is blocking and might cause issues in a large async app.
        # For a true async app, you'd use a library like `aiohttp`.
        # For now, we'll simulate async by just using `await asyncio.sleep(0.1)`
        # to yield control, though the actual network call is blocking.
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - URL: {url} - Response: {http_err.response.text}")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err} - URL: {url}")
        return None
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err} - URL: {url}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected request error occurred: {req_err} - URL: {url}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e} - URL: {url}")
        return None
    finally:
        # Add a small delay to respect API rate limits (Moralis Starter: 40,000 CU/day)
        # This is a simple way to avoid hitting limits too quickly.
        await asyncio.sleep(0.1) # Yield control in async context

async def get_new_tokens_by_exchange(exchange: str = "Raydium", limit: int = 10) -> list | None:
    """
    Retrieves newly listed tokens on a specific exchange.
    Moralis API: /token/mainnet/exchange/{exchange}/new [4]
    Args:
        exchange (str): The name of the exchange (e.g., "Raydium", "Jupiter").
        limit (int): Number of tokens to retrieve.
    Returns:
        list | None: A list of new token dictionaries, or None if an error occurs.
    """
    print(f"Fetching new tokens from {exchange}...")
    url = f"{MORALIS_BASE_URL}/token/mainnet/exchange/{exchange}/new"
    params = {"limit": limit}
    response_data = await _make_moralis_request(url, params)
    if response_data and isinstance(response_data, list):
        print(f"Found {len(response_data)} new tokens from {exchange}.")
        return response_data
    return None

async def get_token_top_holders(token_mint_address: str, limit: int = 10) -> list | None:
    """
    Retrieves the top holders for a specific token.
    Moralis API: /token/mainnet/holders/{address} [4]
    Args:
        token_mint_address (str): The mint address of the token.
        limit (int): Number of top holders to retrieve.
    Returns:
        list | None: A list of holder dictionaries, or None.
    """
    print(f"Fetching top holders for token: {token_mint_address}...")
    url = f"{MORALIS_BASE_URL}/token/mainnet/holders/{token_mint_address}"
    params = {"limit": limit}
    response_data = await _make_moralis_request(url, params)
    if response_data and isinstance(response_data, dict) and 'result' in response_data:
        print(f"Found {len(response_data['result'])} top holders for {token_mint_address}.")
        return response_data['result']
    return None

async def get_wallet_profitability(wallet_address: str) -> dict | None:
    """
    Retrieves detailed profitability metrics for a specific wallet.
    Moralis API: /account/:network/:address/profitability [2, 5]
    Note: The exact endpoint for "wallet profitability" might vary or require specific parameters.
    Based on documentation, it's often part of the Wallet API.
    Let's use a common pattern for Moralis Wallet API.
    """
    print(f"Fetching profitability for wallet: {wallet_address}...")
    url = f"{MORALIS_BASE_URL}/account/mainnet/{wallet_address}/profitability"
    response_data = await _make_moralis_request(url)
    if response_data and isinstance(response_data, dict):
        print(f"Successfully fetched profitability for {wallet_address}.")
        return response_data
    return None

async def get_token_metadata(token_mint_address: str) -> dict | None:
    """
    Retrieves metadata for a specific token.
    Moralis API: /token/:network/:address/metadata [2, 6]
    """
    print(f"Fetching token metadata for: {token_mint_address}...")
    url = f"{MORALIS_BASE_URL}/token/mainnet/{token_mint_address}/metadata"
    response_data = await _make_moralis_request(url)
    if response_data and isinstance(response_data, dict):
        print(f"Successfully fetched metadata for token: {token_mint_address}.")
        return response_data
    return None

async def get_token_price(token_mint_address: str) -> dict | None:
    """
    Retrieves the current price of a specific token.
    Moralis API: /token/:network/:address/price [2, 4]
    """
    print(f"Fetching token price for: {token_mint_address}...")
    url = f"{MORALIS_BASE_URL}/token/mainnet/{token_mint_address}/price"
    response_data = await _make_moralis_request(url)
    if response_data and isinstance(response_data, dict):
        print(f"Successfully fetched price for token: {token_mint_address}.")
        return response_data
    return None