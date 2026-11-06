from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare.db'

# ThingSpeak API configuration
THINGSPEAK_CHANNEL_ID = os.getenv('THINGSPEAK_CHANNEL_ID', '3184441')
THINGSPEAK_READ_API_KEY = os.getenv('THINGSPEAK_READ_API_KEY', 'AESSI3XACM5SSR61')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medicine = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(50), nullable=False)  # e.g., "08:00"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.')
            return redirect(url_for('register'))
        new_user = User(name=name, email=email, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    reminders = Reminder.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', reminders=reminders)

@app.route('/add_reminder', methods=['POST'])
@login_required
def add_reminder():
    medicine = request.form.get('medicine')
    time = request.form.get('time')
    new_reminder = Reminder(user_id=current_user.id, medicine=medicine, time=time)
    db.session.add(new_reminder)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/delete_reminder/<int:reminder_id>', methods=['POST'])
@login_required
def delete_reminder(reminder_id):
    reminder = Reminder.query.filter_by(id=reminder_id, user_id=current_user.id).first()
    if reminder:
        db.session.delete(reminder)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    user_message = request.json.get('message')
    # System prompt for healthcare chatbot
    system_prompt = """You are CardioCare AI, a helpful healthcare assistant. Provide accurate, general health advice based on reliable medical knowledge. Always emphasize that you're not a substitute for professional medical advice and recommend consulting a doctor for personalized diagnosis or treatment. Be empathetic, clear, and concise. Focus on cardiovascular health, general wellness, nutrition, exercise, and mental health. If asked about specific medical conditions, suggest seeing a healthcare professional."""
    full_prompt = f"{system_prompt}\n\nUser: {user_message}\n\nCardioCare AI:"
    # Integrate with Ollama Phi3
    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            'model': 'phi3',
            'prompt': full_prompt,
            'stream': False
        })
        bot_response = response.json().get('response', 'Sorry, I couldn\'t process that. Please try again.')
    except:
        bot_response = 'Error connecting to chatbot. Please ensure Ollama is running with Phi3 model.'
    return jsonify({'response': bot_response})

@app.route('/api/sensor_data')
@login_required
def get_sensor_data():
    try:
        url = f"https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds.json?api_key={THINGSPEAK_READ_API_KEY}&results=1"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if 'feeds' in data and data['feeds']:
            latest_feed = data['feeds'][-1]
            sensor_data = {
                'spo2': latest_feed.get('field1', 'N/A'),
                'bpm': latest_feed.get('field2', 'N/A'),
                'temperature': latest_feed.get('field3', 'N/A'),
                'timestamp': latest_feed.get('created_at', 'N/A')
            }
        else:
            sensor_data = {'spo2': 'N/A', 'bpm': 'N/A', 'temperature': 'N/A', 'timestamp': 'N/A'}

        return jsonify(sensor_data)
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to fetch data from ThingSpeak: {str(e)}'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
