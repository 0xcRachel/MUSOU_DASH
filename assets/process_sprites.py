# pyrefly: ignore [missing-import]
import cv2
import numpy as np
import os

def process_image(input_path, output_dir, bg_color=None, fuzz=30):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Could not read {input_path}")
        return

    # If it's 3 channels, add alpha
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    # Background removal using flood fill
    # We assume the background is connected and starts from (0,0)
    h_img, w_img = img.shape[:2]
    mask = np.zeros((h_img + 2, w_img + 2), np.uint8)
    
    # Create a 3-channel version for flood fill
    rgb_img = img[:, :, :3].copy()
    
    # Flood fill from all four corners just in case
    for seed in [(0, 0), (w_img-1, 0), (0, h_img-1), (w_img-1, h_img-1)]:
        cv2.floodFill(rgb_img, mask, seed, (0, 0, 0), 
                      loDiff=(fuzz, fuzz, fuzz), upDiff=(fuzz, fuzz, fuzz))
    
    # The mask (excluding the padding) identifies the background
    bg_mask = mask[1:-1, 1:-1]
    img[bg_mask > 0, 3] = 0

    # Find contours
    # Use the alpha channel as the mask for contours
    alpha = img[:, :, 3]
    contours, _ = cv2.findContours(alpha, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter and collect ROIs
    parts = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # Filter out text and noise
        # (w > 30 and h > 30) captures square decorations
        # (w > 80 or h > 80) captures thin pipes or tall objects
        if (w > 30 and h > 30) or (w > 80 or h > 80):
            # Check if it's the preview box (very large)
            if w > 400 and h > 300:
                pass
            parts.append((x, y, w, h))

    # Sort parts: first by Y (roughly rows), then by X
    parts.sort(key=lambda b: (b[1] // 50, b[0]))

    count = 0
    for x, y, w, h in parts:
        # If it's a very large blob, it might contain text labels we want to skip
        # but for pipes, we want to keep them.
        # Let's try to crop a bit more aggressively to avoid text if possible
        # or just keep it as is.
        roi = img[y:y+h, x:x+w]
        
        # Check if ROI is mostly transparent or sparse (like text)
        # Pipes and decorations are solid (density > 100)
        # Text labels are sparse (density < 50)
        density = np.mean(roi[:, :, 3])
        # print(f"File: {os.path.basename(input_path)}, Part: {count}, Size: {w}x{h}, Density: {density:.2f}")
        if density < 60: # Increased threshold
            continue

        filename = f"{os.path.splitext(os.path.basename(input_path))[0]}_{count:03d}.png"
        cv2.imwrite(os.path.join(output_dir, filename), roi)
        count += 1
    
    print(f"Extracted {count} parts from {input_path}")
    
    print(f"Extracted {count} parts from {input_path}")

# Paths
assets_dir = "/run/media/Rachel/01D9B9EAC9653800/MUSOU_DASH/assets"
char_output_dir = os.path.join(assets_dir, "images/charcter")
obs_output_dir = os.path.join(assets_dir, "images/obstacles")
bg_output_dir = os.path.join(assets_dir, "images/background")

for d in [char_output_dir, obs_output_dir, bg_output_dir]:
    if not os.path.exists(d):
        os.makedirs(d)

# Process animations.png
process_image(os.path.join(assets_dir, "animations.png"), char_output_dir, fuzz=5)

# Process char.png
process_image(os.path.join(assets_dir, "char.png"), char_output_dir, fuzz=5)

# Process prs.png
process_image(os.path.join(assets_dir, "prs.png"), obs_output_dir, fuzz=5)

# Move the largest prs sprite (the preview) to background
prs_files = [f for f in os.listdir(obs_output_dir) if f.startswith("prs_")]
if prs_files:
    # Sort by size to find the preview (it's the largest)
    prs_files.sort(key=lambda f: os.path.getsize(os.path.join(obs_output_dir, f)), reverse=True)
    # Move the largest one
    largest = prs_files[0]
    os.rename(os.path.join(obs_output_dir, largest), os.path.join(bg_output_dir, "city_preview.png"))
    print(f"Moved {largest} to background/city_preview.png")
