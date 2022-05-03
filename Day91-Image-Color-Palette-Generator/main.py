from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import numpy as np
from PIL import Image

dir_path = 'static/uploaded_images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = dir_path
app.config['SECRET_KEY'] = 'afkjhakfakjsdjka'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

img_path = None

@app.route("/", methods=['GET', 'POST'])
def home():
    global img_path

    if request.method == 'POST':
        file = request.files['img_file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        img_path = dir_path + '/' + filename

        return redirect(url_for('home'))

    elif request.method == 'GET' and img_path:
        img = np.array(Image.open(img_path).convert('RGB'))

        # For png, delete opacity column
        if img.shape[2] == 4:
            img = np.delete(img, 3, 2)

        img = img.reshape(-1, 3)

        # Counting all the unique colors
        (unique, count) = np.unique(img, axis=0, return_counts=True)

        # turn two separate variables into tuple (color code, its corresponding count)
        color_tuple = list(zip(unique, count))

        # sort the colors in descending order of count
        color_tuple = sorted(color_tuple, key=lambda x: x[1], reverse=True)

        # extract the top 10 colors, turn the color code from ndarray to python list of int.
        top_ten_colors = [color[0].astype(int).tolist() for color in color_tuple[:10]]
        print(top_ten_colors)
        return render_template('index.html', colors=top_ten_colors, imgpath=img_path)

    return render_template('index.html')


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % tuple(rgb)

if __name__ == "__main__":
    app.run(debug=True)