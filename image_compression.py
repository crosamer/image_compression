from flask import Flask, render_template, request, send_file
import os
import time
from werkzeug.utils import secure_filename
from utils import compress_image_svd
from PIL import Image
import numpy as np
from shutil import copyfile

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_IMAGE = 'static/output.png'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        k = int(request.form['k'])
        image_file = request.files['image']
        if image_file:
            filename = secure_filename(image_file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(path)
            
            static_original_path = os.path.join('static', filename)
            copyfile(path, static_original_path)

            start_time = time.time()
            original, compressed = compress_image_svd(path, k)
            runtime = time.time() - start_time

            compressed_img = Image.fromarray(compressed)
            compressed_img.save(OUTPUT_IMAGE)

            orig_pixels = original.shape[0] * original.shape[1]
            comp_pixels = k * (original.shape[0] + original.shape[1] + 1)
            compression_ratio = 100 * (1 - comp_pixels / orig_pixels)

            return render_template('index.html',
                original_path=static_original_path,
                output_path=OUTPUT_IMAGE,
                runtime=round(runtime, 4),
                compression=round(compression_ratio, 2))
    return render_template('index.html')

@app.route('/download')
def download():
    return send_file(OUTPUT_IMAGE, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
