import websocket
import uuid
import json
import urllib.request
import urllib.parse
import random
import os
from tqdm import tqdm # Professional Progress Tracking
from dotenv import load_dotenv

load_dotenv()

SERVER_ADDRESS = os.getenv("COMFYUI_SERVER", "localhost:8188")
OUTPUT_FOLDER = os.getenv("OUTPUT_DIR", "final_showcase")
CLIENT_ID = str(uuid.uuid4())

class VulcanDirector:
    def __init__(self, server_address, client_id):
        self.server_address = server_address
        self.client_id = client_id
        self.ws = websocket.WebSocket()

    def connect(self):
        try:
            # Added a longer timeout for the initial handshake
            self.ws.connect(f"ws://{self.server_address}/ws?clientId={self.client_id}", timeout=60)
            print(f"📡 Connected to Engine: {self.server_address}")
        except Exception as e:
            print(f"❌ Connection Failed: {e}")
            raise

    def queue_prompt(self, prompt_workflow):
        p = {"prompt": prompt_workflow, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{self.server_address}/prompt", data=data)
        return json.loads(urllib.request.urlopen(req).read())

    def get_images(self, workflow, scene_name):
        prompt_id = self.queue_prompt(workflow)['prompt_id']
        pbar = None # Initialize Progress Bar
        
        while True:
            out = self.ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                
                # TRACKING SYSTEM: The "100% Bar" you were missing
                if message['type'] == 'progress':
                    data = message['data']
                    if pbar is None:
                        pbar = tqdm(total=data['max'], desc=f"🎨 Rendering {scene_name}", unit="step")
                    pbar.n = data['value']
                    pbar.refresh()

                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        if pbar: pbar.close()
                        break 
            else:
                continue

        with urllib.request.urlopen(f"http://{self.server_address}/history/{prompt_id}") as response:
            return json.loads(response.read())[prompt_id]['outputs']

    def save_output(self, node_outputs, scene_name, index):
        """Resilient saving logic to handle post-generation I/O lag."""
        if not os.path.exists(OUTPUT_FOLDER): os.makedirs(OUTPUT_FOLDER)
        
        for node_id, output in node_outputs.items():
            if 'images' in output:
                for img in output['images']:
                    params = urllib.parse.urlencode({
                        "filename": img['filename'], 
                        "subfolder": img['subfolder'], 
                        "type": img['type']
                    })
                    
                    # RETRY LOGIC: Attempt to download 3 times if the GPU is lagging
                    for attempt in range(3):
                        try:
                            url = f"http://{self.server_address}/view?{params}"
                            with urllib.request.urlopen(url, timeout=30) as resp:
                                filename = f"{OUTPUT_FOLDER}/{str(index).zfill(2)}_{scene_name}.png"
                                with open(filename, "wb") as f:
                                    f.write(resp.read())
                                print(f"✅ Successfully Retrieved: {filename}")
                                return # Success, exit retry loop
                        except Exception as e:
                            print(f"⚠️ Retrieval Attempt {attempt+1} failed: {e}. Retrying...")
                            time.sleep(5) # Wait for Windows I/O to stabilize
                    
                    print(f"❌ Failed to retrieve {scene_name} after 3 attempts.")

# --- SCENARIOS (Ensure these names match your previous setup) ---
SCENARIOS = [
    {"name": "Corporate_CEO", "prompt": "Caitlyn as a tech CEO giving a keynote speech, modern auditorium, confident smile."},
    {"name": "Coffee_Ad", "prompt": "Caitlyn holding a steaming ceramic coffee cup, cozy sweater, rainy cafe window."}
]

if __name__ == "__main__":
    director = VulcanDirector(SERVER_ADDRESS, CLIENT_ID)
    director.connect()

    with open("workflows/flux_api_workflow.json", "r", encoding="utf-8") as f:
        workflow_dag = json.load(f)

    for i, scene in enumerate(SCENARIOS):
        workflow_dag["6"]["inputs"]["text"] = scene['prompt']
        workflow_dag["3"]["inputs"]["seed"] = random.randint(1, 10**12)

        try:
            # Pass scene_name to the progress bar handler
            outputs = director.get_images(workflow_dag, scene['name'])
            director.save_output(outputs, scene['name'], i + 1)
        except Exception as e:
            print(f"\n⚠️ Generation failed: {e}")
            # Reconnect if the peer reset the connection
            if "104" in str(e):
                print("🔄 Attempting to reconnect to Engine...")
                director.connect()
            continue