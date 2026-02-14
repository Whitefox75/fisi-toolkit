from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

# Config
size = 512  # Higher res for better quality
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Colors
col_bg_start = (30, 60, 114)   # Deep Blue
col_bg_end = (42, 82, 152)     # Lighter Blue
col_accent = (0, 210, 255)     # Cyan Neon
col_white = (255, 255, 255)

center = size // 2

def draw_gradient_circle(draw, center, radius, color1, color2):
    # Simple radial gradient simulation
    for r in range(radius, 0, -1):
        ratio = r / radius
        r_val = int(color1[0] * ratio + color2[0] * (1 - ratio))
        g_val = int(color1[1] * ratio + color2[1] * (1 - ratio))
        b_val = int(color1[2] * ratio + color2[2] * (1 - ratio))
        draw.ellipse([center[0]-r, center[1]-r, center[0]+r, center[1]+r], fill=(r_val, g_val, b_val))

# Draw Background (Modern Rounded Rec or Circle)
# Let's do a smooth rounded rect (Squircle-ish)
bg_r = 240
draw.ellipse([center-bg_r, center-bg_r, center+bg_r, center+bg_r], fill=col_bg_start)

# Add stylized "Network" nodes
nodes = [
    (center, center - 120),
    (center - 100, center + 60),
    (center + 100, center + 60)
]

# Draw Connections
for i in range(len(nodes)):
    p1 = nodes[i]
    p2 = nodes[(i + 1) % len(nodes)]
    draw.line([p1, p2], fill=col_accent, width=15)
    
# Draw Center Connection
draw.line([nodes[0], (center, center+20)], fill=col_accent, width=8)

# Draw Nodes
for x, y in nodes:
    r = 35
    draw.ellipse([x-r, y-r, x+r, y+r], fill=col_white)
    r_inner = 20
    draw.ellipse([x-r_inner, y-r_inner, x+r_inner, y+r_inner], fill=col_bg_start)

# Central Element (Chip/Server representation)
rect_w, rect_h = 140, 100
draw.rounded_rectangle([center-rect_w//2, center-rect_h//2 + 20, center+rect_w//2, center+rect_h//2 + 20], radius=20, fill=col_white)
draw.rounded_rectangle([center-rect_w//2 + 10, center-rect_h//2 + 30, center+rect_w//2 - 10, center+rect_h//2 + 10], radius=10, fill=col_bg_end)

# Save
img = img.resize((256, 256), Image.Resampling.LANCZOS) # Downscale for AA
img.save('icon.png')
print("Modern icon created.")
