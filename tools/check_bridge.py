import os
from dotenv import load_dotenv
import urllib.request

# Explicitly point to the .env in the root
env_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path=env_path)

def verify_system():
    server = os.getenv("COMFYUI_SERVER")
    
    if not server:
        print("❌ [CRITICAL]: COMFYUI_SERVER not found in .env file!")
        print(f"   Searching in: {env_path}")
        return

    print(f"🔍 Testing connection to: http://{server}/history")
    
    try:
        # Use a short timeout to prevent hanging
        with urllib.request.urlopen(f"http://{server}/history", timeout=3) as resp:
            print(f"✅ [NETWORK]: Successfully connected to Windows Engine.")
    except Exception as e:
        print(f"❌ [NETWORK]: Connection failed.")
        print(f"   Error: {e}")
        print("   TIP: Ensure ComfyUI is running on Windows with --listen 0.0.0.0")

if __name__ == "__main__":
    verify_system()