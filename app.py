from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import sys
import codecs
import requests
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Setup database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="calorie_db"
)

cursor = db.cursor(dictionary=True)

# Fix encoding issue for Windows systems
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'key123'  # Ganti dengan yang lebih aman di produksi

# Load the trained model (gunakan path yang sesuai)
model = load_model(r"D:\Project AI Final\project\model\model_trained_101class.h5")

# Class map (101 classes)
class_map = {
    idx: label for idx, label in enumerate([
        'Apple pie', 'Baby back ribs', 'Baklava', 'Beef carpaccio', 'Beef tartare',
        'Beet salad', 'Beignets', 'Bibimbap', 'Bread pudding', 'Breakfast burrito',
        'Bruschetta', 'Caesar salad', 'Cannoli', 'Caprese salad', 'Carrot cake',
        'Ceviche', 'Cheesecake', 'Cheese plate', 'Chicken curry', 'Chicken quesadilla',
        'Chicken wings', 'Chocolate cake', 'Chocolate mousse', 'Churros', 'Clam chowder',
        'Club sandwich', 'Crab cakes', 'Creme brulee', 'Croque madame', 'Cup cakes',
        'Deviled eggs', 'Donuts', 'Dumplings', 'Edamame', 'Eggs benedict', 'Escargots',
        'Falafel', 'Filet mignon', 'Fish and chips', 'Foie gras', 'French fries',
        'French onion soup', 'French toast', 'Fried calamari', 'Fried rice', 'Frozen yogurt',
        'Garlic bread', 'Gnocchi', 'Greek salad', 'Grilled cheese sandwich', 'Grilled salmon',
        'Guacamole', 'Gyoza', 'Hamburger', 'Hot and sour soup', 'Hot dog', 'Huevos rancheros',
        'Hummus', 'Ice cream', 'Lasagna', 'Lobster bisque', 'Lobster roll sandwich',
        'Macaroni and cheese', 'Macarons', 'Miso soup', 'Mussels', 'Nachos', 'Omelette',
        'Onion rings', 'Oysters', 'Pad thai', 'Paella', 'Pancakes', 'Panna cotta',
        'Peking duck', 'Pho', 'Pizza', 'Pork chop', 'Poutine', 'Prime rib',
        'Pulled pork sandwich', 'Ramen', 'Ravioli', 'Red velvet cake', 'Risotto', 'Samosa',
        'Sashimi', 'Scallops', 'Seaweed salad', 'Shrimp and grits', 'Spaghetti bolognese',
        'Spaghetti carbonara', 'Spring rolls', 'Steak', 'Strawberry shortcake', 'Sushi',
        'Tacos', 'Takoyaki', 'Tiramisu', 'Tuna tartare', 'Waffles'
    ])
}

# Nutritionix API Credentials
app_id = "ef34f3e3"
api_key = "7eeb1ab0716eb2985817786796409b0b"

def get_calories(food_item):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": app_id,
        "x-app-key": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "query": food_item,
        "timezone": "US/Eastern"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        food_data = result["foods"][0]
        calories = food_data["nf_calories"]
        serving_weight = food_data["serving_weight_grams"]
        calories_per_100g = (calories / serving_weight) * 100
        return f"{calories_per_100g:.2f} calories per 100 grams"
    else:
        return "Error retrieving data"

def is_good_for_diet(calories_per_100g):
    try:
        calories = float(calories_per_100g.split()[0])  # Extract calorie value
    except:
        return "❓ Data kalori tidak valid"
    if calories < 200:
        return "✔️ Bagus untuk diet (Rendah Kalori)"
    elif calories <= 500:
        return "⚠️ Cocok untuk diet (Sedang Kalori)"
    else:
        return "❌ Kurang cocok untuk diet (Tinggi Kalori)"

# Allowed file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route("/", endpoint="home")
def home():
    return render_template("coba.html")

@app.route('/mainhome')
def main_home():
    return render_template("index.html")

@app.route('/aboutpage')
def about_page():
    return render_template('aboutpage.html')

@app.route('/aboutpage1')
def about_page1():
    return render_template('aboutpage copy.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['email'] = user['email']
            return redirect(url_for('main_home'))
        else:
            error = "Email atau password salah"
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
            db.commit()
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            return render_template('signup.html', error="Email sudah terdaftar")
    return render_template('signup.html')

@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        new_password = request.form['newPassword']
        confirm_password = request.form['confirmPassword']

        if new_password != confirm_password:
            return render_template('forgotpassword.html', message='Passwords do not match.', color='#e53935')

        # NOTE: Implement actual password reset logic here!
        print(f"Password berhasil direset: {new_password}")

        return redirect(url_for('login'))
    return render_template('forgotpassword.html')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@app.route('/history')
def history():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    cursor.execute("""
        SELECT id, food_name, calories_per_100g AS calories, diet_suitability AS diet_status, image_path
        FROM prediction_history
        WHERE user_id = %s
        ORDER BY prediction_date DESC
    """, (user_id,))
    records = cursor.fetchall()
    return render_template('history.html', records=records)

@app.route('/delete_history/<int:id>', methods=['POST'])
def delete_history(id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    cursor.execute("SELECT image_path FROM prediction_history WHERE id = %s AND user_id = %s", (id, user_id))
    record = cursor.fetchone()
    if record:
        image_path = os.path.join('uploads', record['image_path'])
        cursor.execute("DELETE FROM prediction_history WHERE id = %s AND user_id = %s", (id, user_id))
        db.commit()
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            print(f"Gagal menghapus file: {e}")
    return redirect(url_for('history'))

@app.before_request
def require_login():
    allowed_routes = ['home', 'login', 'signup', 'forgot_password', 'static']
    if request.endpoint not in allowed_routes and 'user_id' not in session:
        return redirect(url_for('login'))

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"})

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only JPG, JPEG, and PNG are allowed."})

    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)
    
    # Timestamp supaya nama file unik
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    saved_filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_folder, saved_filename)
    file.save(file_path)

    try:
        image = load_img(file_path, target_size=(224, 224))
        image_array = img_to_array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        predictions = model.predict(image_array)
        predicted_class = class_map[np.argmax(predictions)]
        confidence = np.max(predictions)

        calorie_info = get_calories(predicted_class)
        diet_evaluation = is_good_for_diet(calorie_info)

        user_id = session.get('user_id')
        if user_id:
            try:
                calories = float(calorie_info.split()[0])
                prediction_date = datetime.now()
                cursor.execute("""
                    INSERT INTO prediction_history (
                        user_id, image_path, food_name, calories_per_100g, diet_suitability, prediction_date
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    user_id,
                    saved_filename,
                    predicted_class,
                    calories,
                    diet_evaluation,
                    prediction_date
                ))
                db.commit()
            except Exception as db_err:
                print(f"Database insert error: {db_err}")

        return jsonify({
            "foodName": predicted_class,
            "caloriesPerGram": calorie_info,
            "dietSuitability": diet_evaluation,
            "confidence": float(confidence),
            "image": saved_filename
        })

    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({"error": "Failed to process image"})

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
