# Full Python App (Flask-based Image Editor with Text Change Support)

# File: app.py
from flask import Flask, request, send_file, render_template
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import io
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image = request.files["image"]
        description = request.form["description"].strip().lower()

        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_path)

        # Load image with PIL
        pil_image = Image.open(image_path).convert("RGB")

        # OCR to find text
        detected_text = pytesseract.image_to_string(pil_image)

        # Simple logic: replace first detected word from description
        words = description.split("replace")
        if len(words) == 2:
            parts = words[1].strip().split("with")
            if len(parts) == 2:
                old_text = parts[0].strip(" ' \"")
                new_text = parts[1].strip(" ' \"")

                # Draw over old text
                boxes = pytesseract.image_to_data(pil_image, output_type=pytesseract.Output.DICT)
                draw = ImageDraw.Draw(pil_image)
                font = ImageFont.load_default()

                for i, word in enumerate(boxes['text']):
                    if word.strip().lower() == old_text.lower():
                        x, y, w, h = boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
                        draw.rectangle([x, y, x + w, y + h], fill="white")
                        draw.text((x, y), new_text, fill="black", font=font)
                        break

        # Save modified image to memory
        img_io = io.BytesIO()
        pil_image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')

    return render_template("index.html")
