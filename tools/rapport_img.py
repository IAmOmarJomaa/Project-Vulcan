import os
import glob
from PIL import Image, ImageOps

# --- CONFIGURATION ---
# Chemin vers ton dossier d'images (Format WSL)
IMAGE_FOLDER = "/home/iamomarjomaa/gen_ai/selections"
OUTPUT_FILE = "dataset_album_pro.jpg"

# Combien d'images veux-tu par ligne ? (3 ou 4 est conseillé)
IMAGES_PER_ROW = 3

# Largeur cible de l'image finale en pixels (3000 = haute résolution pour impression)
TARGET_WIDTH = 3000

# Espace entre les images (padding) en pixels
PADDING = 20
# ---------------------


def create_smart_collage(image_paths, output_path, imgs_per_row, target_width, padding):
    """Crée un collage intelligent en respectant les ratios."""
    
    # 1. Charger toutes les images en mémoire
    loaded_images = []
    print(f"📂 Chargement de {len(image_paths)} images...")
    for p in image_paths:
        try:
            img = Image.open(p)
            # Convertir en RGB si nécessaire (pour éviter problèmes avec PNG transparents)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            loaded_images.append(img)
        except Exception as e:
            print(f"⚠️ Impossible de lire {p}: {e}")

    if not loaded_images:
        print("❌ Aucune image valide trouvée.")
        exit()

    # Limiter au nombre d'images souhaité pour le rapport (ex: les 10 premières)
    # loaded_images = loaded_images[:12] 

    # 2. Diviser en lignes (chunks)
    rows = [loaded_images[i:i + imgs_per_row] for i in range(0, len(loaded_images), imgs_per_row)]
    
    processed_rows = []
    total_height = 0

    print(f"📐 Calcul de la mise en page pour {len(rows)} lignes...")

    # 3. Traiter chaque ligne
    for row_imgs in rows:
        # Calculer la largeur disponible pour les images (largeur totale - les espaces)
        available_width = target_width - (padding * (len(row_imgs) + 1))
        
        # Somme des ratios d'aspect (largeur / hauteur) de la ligne
        # Cela permet de trouver la hauteur commune idéale
        aspect_ratio_sum = sum([img.width / img.height for img in row_imgs])
        
        # Hauteur idéale pour que cette ligne remplisse exactement la largeur disponible
        row_height = int(available_width / aspect_ratio_sum)
        
        resized_imgs_in_row = []
        current_row_width = 0
        
        # Redimensionner chaque image de la ligne à cette nouvelle hauteur
        for img in row_imgs:
            new_width = int(img.width * (row_height / img.height))
            resized_img = img.resize((new_width, row_height), Image.Resampling.LANCZOS)
            resized_imgs_in_row.append(resized_img)
            current_row_width += new_width

        processed_rows.append({
            'images': resized_imgs_in_row,
            'height': row_height,
            'width': current_row_width # Largeur réelle occupée par les images
        })
        total_height += row_height + padding

    # Ajouter le padding final en bas
    total_height += padding

    # 4. Créer la toile blanche finale
    print(f"🎨 Création de l'image finale ({target_width}x{total_height} px)...")
    collage = Image.new('RGB', (target_width, total_height), 'white')
    
    current_y = padding

    # 5. Coller les images
    for row_data in processed_rows:
        # Centrer la ligne horizontalement si elle est un peu moins large que le target
        row_content_width = row_data['width'] + (padding * (len(row_data['images']) - 1))
        start_x = (target_width - row_content_width) // 2
        
        current_x = start_x
        
        for img in row_data['images']:
            collage.paste(img, (current_x, current_y))
            current_x += img.width + padding
            
        current_y += row_data['height'] + padding

    # 6. Sauvegarder
    collage.save(output_path, quality=95)
    print(f"✅ Succès ! Album sauvegardé sous : {output_path}")


# --- Exécution ---
if __name__ == "__main__":
    # Vérifier le chemin
    if not os.path.exists(IMAGE_FOLDER):
        print(f"❌ Erreur : Le dossier {IMAGE_FOLDER} n'existe pas.")
        exit()

    # Trouver les images
    extensions = ["*.png", "*.jpg", "*.jpeg", "*.PNG", "*.JPG"]
    image_files = []
    for ext in extensions:
        image_files.extend(glob.glob(os.path.join(IMAGE_FOLDER, ext)))
    
    # Trier pour avoir un ordre cohérent
    image_files.sort()

    if not image_files:
        print("❌ Erreur : Aucune image trouvée dans le dossier.")
        exit()
        
    # Lancer la création
    create_smart_collage(image_files, OUTPUT_FILE, IMAGES_PER_ROW, TARGET_WIDTH, PADDING)