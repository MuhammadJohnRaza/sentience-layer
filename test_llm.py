import asyncio
import os
import sys

# Ensure backend/python is in path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'python'))

from backend.python.antigravity_client import AntigravityClient
from backend.python.config import settings

async def main():
    print(f"Testing API Key: {settings.OPENROUTER_API_KEY[:10]}... (length: {len(str(settings.OPENROUTER_API_KEY))})")
    
    client = AntigravityClient()
    print(f"Connecting to base URL: {client.base_url}")
    
    print("\n--- Testing OpenRouter Generation (meta-llama/Llama-3-8b-instruct) ---")
    response = await client.generate("Hello, just say 'Connection successful' and nothing else.")
    
    try:
        if response.success:
            print("[SUCCESS] Connection successful!")
            print(f"Latency: {response.latency_ms:.2f}ms")
            try:
                message = response.data.get('choices', [{}])[0].get('message', {}).get('content', '')
                print(f"Response: {message}")
            except Exception as e:
                print(f"Response object: {response.data}")
        else:
            print("[FAILED] Request failed!")
            print(f"Error: {response.error}")
    finally:
        await client.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
