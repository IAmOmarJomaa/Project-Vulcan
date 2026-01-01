import websocket # pip install websocket-client
import uuid
import json
import urllib.request
import urllib.parse
import random
import os
import sys

# --- CONFIGURATION ---
# Your Windows IP (Check if it changed!)
SERVER_ADDRESS = "192.168.112.1:8188" 
CLIENT_ID = str(uuid.uuid4())

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": CLIENT_ID}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/view?{url_values}") as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as response:
        return json.loads(response.read())

def get_images(ws, workflow):
    prompt_id = queue_prompt(workflow)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break # Execution is done
        else:
            continue

    history = get_history(prompt_id)[prompt_id]
    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        if 'images' in node_output:
            images_output = []
            for image in node_output['images']:
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images

# --- MAIN LOOP ---
if __name__ == "__main__":
    # 1. Load Workflow
    if not os.path.exists("flux_api_workflow.json"):
        print("❌ Error: 'flux_api_workflow.json' missing.")
        sys.exit()

    with open("flux_api_workflow.json", "r", encoding="utf-8") as f:
        workflow = json.load(f)

    # 2. Connect
    print(f"📡 Connected to Engine at {SERVER_ADDRESS}")
    ws = websocket.WebSocket()
    try:
        ws.connect(f"ws://{SERVER_ADDRESS}/ws?clientId={CLIENT_ID}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        sys.exit()

    print("🚀 Instant Director Ready! (Type 'exit' to quit)")
    print("------------------------------------------------")

    # 3. Interactive Loop
    while True:
        try:
            # Get input from user
            user_input = input("\n🎨 Enter Prompt: ")
            
            if user_input.lower() in ["exit", "quit", "q"]:
                print("👋 Goodbye!")
                break
            
            if not user_input.strip():
                continue

            print("⏳ Generating...")

            # Inject Prompt & Random Seed
            workflow["6"]["inputs"]["text"] = user_input
            workflow["3"]["inputs"]["seed"] = random.randint(1, 10**10)

            # Execute
            images = get_images(ws, workflow)

            # Save & Open
            for node_id in images:
                for image_data in images[node_id]:
                    # Create a clean filename from the first few words of the prompt
                    safe_name = "".join([c for c in user_input[:20] if c.isalnum() or c==' ']).strip().replace(" ", "_")
                    filename = f"instant_{safe_name}.png"
                    
                    with open(filename, "wb") as f:
                        f.write(image_data)
                    
                    print(f"✅ Saved: {filename}")
                    
                    # MAGIC COMMAND: Open image in Windows
                    print("👀 Opening...")
                    os.system(f"explorer.exe {filename}")

        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")