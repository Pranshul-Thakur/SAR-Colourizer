from PIL import Image, ImageEnhance
import numpy as np
from scipy.ndimage import median_filter
import tensorflow as tf
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

generator_model = tf.keras.models.load_model('C:\\Users\\LENOVO\\Desktop\\app\\static.h5')

def despeckle_image(img):
    return median_filter(img, size=3)

def adjust_brightness(img, factor=1.5):
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)

def process_image(img):
    img = img.resize((1024, 1024))
    img = img.convert('RGB')
    img_array = np.array(img) / 255.0
    despeckled_img = despeckle_image(img_array)
    despeckled_img = np.expand_dims(despeckled_img, axis=0)
    
    colorized_img = generator_model.predict(despeckled_img)
    colorized_img = (colorized_img[0] * 255).astype(np.uint8)
    
    colorized_img = Image.fromarray(colorized_img)
    colorized_img = adjust_brightness(colorized_img, factor=0.3)

    return colorized_img

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            img = Image.open(file)
            result_img = process_image(img)
            result_img.save('static/result_image.png')
            return redirect(url_for('result'))

@app.route('/result')
def result():
    return render_template('result.html', img_url='static/result_image.png')

if __name__ == '__main__':
    app.run(debug=True)
