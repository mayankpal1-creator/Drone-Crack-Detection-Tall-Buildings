import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Load image captured by drone
image_path = "data/sample_wall.jpg"
image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError("Input image not found. Place image in data/ folder.")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Reduce noise
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Detect edges (cracks)
edges = cv2.Canny(blur, 50, 150)

# Strengthen cracks
kernel = np.ones((3, 3), np.uint8)
dilated = cv2.dilate(edges, kernel, iterations=1)

# Find crack contours
contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

total_crack_pixels = 0

for cnt in contours:
    length = cv2.arcLength(cnt, False)
    total_crack_pixels += length
    cv2.drawContours(image, [cnt], -1, (0, 0, 255), 2)

# Convert pixels to meters
PIXEL_TO_METER = 0.001  # 1 pixel ≈ 1 mm
crack_length_meters = total_crack_pixels * PIXEL_TO_METER

print(f"Total Crack Length Detected: {crack_length_meters:.2f} meters")

# Save output image
os.makedirs("output", exist_ok=True)
output_path = "output/detected_cracks.png"
cv2.imwrite(output_path, image)

# Display result
plt.figure(figsize=(8, 6))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("Detected Cracks")
plt.axis("off")
plt.show()
