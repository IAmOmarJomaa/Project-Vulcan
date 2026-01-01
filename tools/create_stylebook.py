import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import glob
import textwrap

# --- CONFIGURATION ---
IMAGE_FOLDER = "final_showcase"
OUTPUT_FILE = "Final_Presentation_Board.jpg"
ROWS = 3
COLS = 5
FIG_SIZE = (20, 15) # High resolution size (width, height)

# --- THE DATA (For captions) ---
SCENARIOS = [
    {"name": "Corporate CEO", "prompt": "Caitlyn as a tech CEO giving a keynote speech, modern auditorium, confident smile."},
    {"name": "Coffee Ad", "prompt": "Caitlyn holding a steaming ceramic coffee cup, cozy sweater, rainy window cafe."},
    {"name": "Luxury Perfume", "prompt": "Caitlyn in an elegant evening gown, holding a crystal perfume bottle, studio lighting."},
    {"name": "Fitness Brand", "prompt": "Caitlyn jogging in a modern city park at sunrise, premium athletic wear, dynamic pose."},
    {"name": "Doctor", "prompt": "Caitlyn dressed as a professional doctor with a stethoscope, white coat, hospital background."},
    {"name": "Travel Paris", "prompt": "Caitlyn taking a selfie with the Eiffel Tower, golden hour, chic beret and trench coat."},
    {"name": "Cozy Reading", "prompt": "Caitlyn reading a book in a comfortable armchair, surrounded by plants, library setting."},
    {"name": "Summer Beach", "prompt": "Caitlyn walking on a white sand beach, wearing a white linen dress, sunny day."},
    {"name": "Urban Style", "prompt": "Caitlyn leaning against a brick wall in New York, leather jacket, sunglasses, neon."},
    {"name": "Cooking Chef", "prompt": "Caitlyn in a modern kitchen wearing a chef's apron, preparing a gourmet salad."},
    {"name": "SciFi Cyberpunk", "prompt": "Caitlyn in a futuristic cyberpunk city, neon rain, high-tech tactical jacket."},
    {"name": "Fantasy Elf", "prompt": "Caitlyn as an ethereal elf queen in a magical forest, silver tiara, glowing fireflies."},
    {"name": "Space Explorer", "prompt": "Caitlyn wearing a white space suit inside a spaceship corridor, looking at Earth."},
    {"name": "Victorian Era", "prompt": "Portrait of Caitlyn in 1890s Victorian era clothing, high collar lace dress, sepia."},
    {"name": "Abstract Art", "prompt": "Double exposure artistic portrait of Caitlyn combined with a forest landscape."}
]

def create_grid():
    # 1. Get Images
    # Sort ensures 01 matches Scenario 1, 02 matches Scenario 2, etc.
    image_files = sorted(glob.glob(os.path.join(IMAGE_FOLDER, "*.png")))
    
    if not image_files:
        print("❌ No images found in final_showcase!")
        return

    print(f"🎨 Creating {ROWS}x{COLS} grid from {len(image_files)} images...")

    # 2. Setup Plot
    # constrained_layout helps prevent text overlap automatically
    fig, axes = plt.subplots(ROWS, COLS, figsize=FIG_SIZE, constrained_layout=True)
    
    # Flatten axes array for easy looping
    axes_flat = axes.flatten()

    # 3. Fill the Grid
    for i, ax in enumerate(axes_flat):
        if i < len(image_files) and i < len(SCENARIOS):
            img_path = image_files[i]
            scenario = SCENARIOS[i]
            
            try:
                # Load and Display Image
                img = mpimg.imread(img_path)
                ax.imshow(img)
                
                # --- CAPTION STYLING ---
                # Title (Bold)
                title = scenario['name']
                # Prompt (Wrapped, smaller)
                wrapped_prompt = "\n".join(textwrap.wrap(scenario['prompt'], width=30))
                
                label_text = f"{title}\n\n{wrapped_prompt}"
                
                # Set text below image (xlabel)
                ax.set_xlabel(label_text, fontsize=9, labelpad=10, linespacing=1.4)
                
                # Clean up borders
                ax.set_xticks([]) # Remove X ticks
                ax.set_yticks([]) # Remove Y ticks
                
                # Remove the black box outline (spines)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                    
            except Exception as e:
                print(f"⚠️ Error reading {img_path}: {e}")
        else:
            # Hide unused squares
            ax.axis('off')

    # 4. Add Main Title
    fig.suptitle('PROJECT VULCAN: Digital Twin Scenarios', fontsize=20, weight='bold')

    # 5. Save
    print("💾 Saving high-res image...")
    # facecolor='white' ensures the background is white, not transparent
    plt.savefig(OUTPUT_FILE, dpi=200, facecolor='white')
    print(f"✅ Done! Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    create_grid()