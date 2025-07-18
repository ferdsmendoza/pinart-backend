from flask import Flask, request, jsonify
from PIL import Image
import imagehash
import os

app = Flask(__name__)

HASH_DB_FILE = "hashes.txt"

def load_hashes():
    if not os.path.exists(HASH_DB_FILE):
        return set()
    with open(HASH_DB_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_hash(image_hash):
    with open(HASH_DB_FILE, "a") as f:
        f.write(f"{image_hash}\n")

@app.route('/check_artwork', methods=['POST'])
def check_artwork():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    img_file = request.files['image']
    img = Image.open(img_file.stream)

    uploaded_hash = imagehash.phash(img)
    existing_hashes = load_hashes()

    for saved in existing_hashes:
        if uploaded_hash - imagehash.hex_to_hash(saved) < 5:
            return jsonify({'similar': True})

    save_hash(str(uploaded_hash))
    return jsonify({'similar': False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

