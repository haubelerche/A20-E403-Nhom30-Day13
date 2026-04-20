import os
from dotenv import load_dotenv
from langfuse import Langfuse

# Load environment variables
load_dotenv()

public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
secret_key = os.getenv("LANGFUSE_SECRET_KEY")
host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

print(f"--- Langfuse Diagnostics ---")
print(f"PUBLIC_KEY: {public_key[:10]}..." if public_key else "PUBLIC_KEY: MISSING")
print(f"SECRET_KEY: {secret_key[:10]}..." if secret_key else "SECRET_KEY: MISSING")
print(f"HOST: {host}")

if not public_key or not secret_key:
    print("\n[ERROR] Missing Langfuse credentials in .env file!")
    exit(1)

try:
    langfuse = Langfuse(
        public_key=public_key,
        secret_key=secret_key,
        host=host,
        debug=True # Enable debug mode
    )
    
    print("\nAttempting to send a test trace...")
    trace = langfuse.trace(name="connection-test", user_id="diag-user")
    trace.event(name="test-event", metadata={"status": "checking-connection"})
    
    # Flush to send immediately
    langfuse.flush()
    print("\n[SUCCESS] Test trace sent! Please check your Langfuse Dashboard for 'connection-test'.")
    print("If it still doesn't appear, check if your Project ID matches the keys provided.")

except Exception as e:
    print(f"\n[CRITICAL ERROR] Failed to connect/send to Langfuse: {e}")
