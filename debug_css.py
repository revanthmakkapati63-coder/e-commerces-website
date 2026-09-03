from app import create_app
app = create_app()

# Read the CSS file and look for any rules hiding images
with open('app/static/css/style.css', 'r') as f:
    css = f.read()

print("=== Checking CSS for image-hiding rules ===")

# Look for display:none, visibility:hidden, opacity rules on .card-img-top or img
# Check for display:none
if 'display: none' in css:
    print("WARNING: Found 'display: none' in CSS")

# Check for visibility:hidden
if 'visibility: hidden' in css:
    print("WARNING: Found 'visibility: hidden' in CSS")

# Check for opacity:0 - THIS WAS THE ORIGINAL BUG!
if 'opacity: 0' in css or 'opacity:0' in css:
    print("WARNING: Found 'opacity: 0' in CSS - THIS WAS THE ORIGINAL BUG!")

# Check .card-img-top rules
if '.card-img-top' in css:
    print(" .card-img-top rule exists")

# Check img rules
if 'img' in css.lower():
    print(" img rule exists")

# Look for position-related hiding
if 'opacity: .1' in css or 'opacity:0.1' in css:
    print("WARNING: Found very low opacity")

print("\n=== Looking for problematic patterns ===")

problematic_patterns = [
    'opacity:',
    'display:',
    'visibility:',
    'filter:',
]

for pattern in problematic_patterns:
    count = css.lower().count(pattern.lower())
    print(f"'{pattern}' appears {count} times")

print("\n=== Key .card-img-top rules ===")
import re
height_match = re.search(r'\.card-img-top\s*\{[^}]*height:\s*([^;]+)', css)
if height_match:
    print(f"height: {height_match.group(1)}")

object_fit = re.search(r'object-fit:\s*([^;]+)', css)
if object_fit:
    print(f"object-fit: {object_fit.group(1)}")

# Check for any position:absolute that might hide
pos_match = re.search(r'position:\s*absolute', css)
if pos_match:
    print("WARNING: position: absolute found")

# Check for z-index that might hide
z_match = re.search(r'z-index:\s*(\d+)', css)
if z_match:
    print(f"z-index: {z_match.group(1)}")

print("\n=== Full .card-img-top rule content ===")
# Find and print the .card-img-top block
import re
card_img_match = re.search(r'\.card-img-top\s*\{[^}]*\}', css)
if card_img_match:
    print(card_img_match.group(0))
else:
    print("No .card-img-top block found")

print("\n=== Check for .product-card-img ===")
product_img_match = re.search(r'\.product-card-img\s*\{[^}]*\}', css)
if product_img_match:
    print(product_img_match.group(0))
else:
    print("No .product-card-img block found (using Bootstrap classes)")

print("\n=== Check for animation keyframes ===")
anim_match = re.search(r'@keyframes', css)
if anim_match:
    print("WARNING: @keyframes found in CSS")
else:
    print("No @keyframes found (good - animations removed)")

print("\n=== Check for animation-fill-mode ===")
afm_match = re.search(r'animation-fill-mode', css)
if afm_match:
    print("WARNING: animation-fill-mode found")
else:
    print("No animation-fill-mode found (good)")