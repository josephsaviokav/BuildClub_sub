

import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# reading the image from the assets folder

image_path = "../assets/tom.jpg" 
image = cv2.imread(image_path)

#  converting BGR to RGB for matplotlib display
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# applying median blur for smooth output
image_blurred = cv2.medianBlur(image_rgb, 5)

#displaying the original and blurred images
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.imshow(image_rgb)
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(image_blurred)
plt.title('Blurred Image')
plt.axis('off')
plt.tight_layout()
plt.savefig('step1_original_blurred.png')
plt.close()  #closing instead of showing

#creating a Look-Up Table (LUT) for posterization
# n = number of levels I want to quantize colors to
n = 5  #  change this value

#creating a LUT that maps 0-255 to n evenly spaced values
lut = np.zeros(256, dtype=np.uint8)
for i in range(256):
    #mapping pixel value i to nearest quantized level
    level = int((i / 255) * (n - 1))  #determining which level (0 to n-1)
    lut[i] = int((level / (n - 1)) * 255)  #mapping back to 0-255 range

print("Look-Up Table (LUT) for n =", n)
print(lut)

#applying the LUT to each channel of the image
# For color images, I need to apply LUT to each BGR channel separately
image_posterized = cv2.LUT(image_blurred, lut)

#displaying the original and posterized images side-by-side
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.imshow(image_rgb)
plt.title(f'Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(image_posterized)
plt.title(f'Posterized Image (n={n})')
plt.axis('off')

plt.tight_layout()
plt.savefig(f'posterization_result_n={n}.png')
plt.close()  #closing instead of showing

#trying different posterization levels
print("\nGenerating posterization with different levels...")
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

levels = [2, 3, 4, 5, 6, 8]
for idx, n_level in enumerate(levels):
    lut_temp = np.zeros(256, dtype=np.uint8)
    for i in range(256):
        level = int((i / 255) * (n_level - 1))
        lut_temp[i] = int((level / (n_level - 1)) * 255)
    
    posterized_temp = cv2.LUT(image_blurred, lut_temp)
    
    row = idx // 3
    col = idx % 3
    axes[row, col].imshow(posterized_temp)
    axes[row, col].set_title(f'Posterized (n={n_level})')
    axes[row, col].axis('off')

plt.tight_layout()
plt.savefig('posterization_comparison.png')
plt.close()  #closing instead of showing

#trying color space transformation (HSV) for striking effects
print("\nApplying color space transformation...")
image_hsv = cv2.cvtColor(image_blurred, cv2.COLOR_RGB2HSV)

#posterizing only the Saturation and Value channels
s_channel = image_hsv[:, :, 1]
v_channel = image_hsv[:, :, 2]

lut_color = np.zeros(256, dtype=np.uint8)
n_color = 4
for i in range(256):
    level = int((i / 255) * (n_color - 1))
    lut_color[i] = int((level / (n_color - 1)) * 255)

image_hsv_posterized = image_hsv.copy()
image_hsv_posterized[:, :, 1] = cv2.LUT(s_channel, lut_color)  #posterizing Saturation
image_hsv_posterized[:, :, 2] = cv2.LUT(v_channel, lut_color)  #posterizing Value

image_hsv_posterized_rgb = cv2.cvtColor(image_hsv_posterized, cv2.COLOR_HSV2RGB)

#displaying the HSV posterization result
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.imshow(image_rgb)
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(image_hsv_posterized_rgb)
plt.title('Posterized (HSV Color Space)')
plt.axis('off')

plt.tight_layout()
plt.savefig('posterization_hsv.png')
plt.close()  #closing instead of showing

print("\nPosterization complete!")
print(f"Images saved:")
print("- step1_original_blurred.png")
print(f"- posterization_result_n={n}.png")
print("- posterization_comparison.png")
print("- posterization_hsv.png")
