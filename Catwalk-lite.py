import time
from plyer import gyroscope, gps
import speech_recognition as sr
import requests

# Twilio for SMS (if preferred)
from twilio.rest import Client

# Constants
MAX_TILT_ANGLE = 45  # Max angle before intervention
EMERGENCY_API_URL = "https://emergency.example.com/report"  # Replace with actual API
THRESHOLD_IMPACT_SOUND = 70  # Sound threshold for accidents (dB)
TWILIO_ACCOUNT_SID = "your_account_sid"  # Replace with your Twilio SID
TWILIO_AUTH_TOKEN = "your_auth_token"  # Replace with your Twilio auth token
TWILIO_PHONE_NUMBER = "+1234567890"  # Replace with your Twilio phone number
EMERGENCY_CONTACT = "+0987654321"  # Replace with emergency contact number


import json
import requests

# Constants
MOTORCYCLE_DATA_API = "https://example.com/motorcycle-data"  # Replace with actual API

def collect_motorcycle_data():
    """
    Collect motorcycle data from the user.
    """
    print("Welcome! Let's configure your motorcycle settings.")
    
    motorcycle_data = {
        "make": input("Enter motorcycle make (e.g., Yamaha): ").strip(),
        "model": input("Enter motorcycle model (e.g., MT-07): ").strip(),
        "year": input("Enter motorcycle year (e.g., 2023): ").strip(),
        "rider_weight": input("Enter rider weight (kg) [Optional]: ").strip() or None,
    }
    
    # Confirm and save locally
    print("\nMotorcycle data collected:")
    print(json.dumps(motorcycle_data, indent=4))
    
    # Save locally
    save_local_data(motorcycle_data)

    # Share with server
    share_motorcycle_data(motorcycle_data)

    return motorcycle_data

def save_local_data(data):
    """
    Save motorcycle data locally.
    """
    try:
        with open("motorcycle_data.json", "w") as file:
            json.dump(data, file)
        print("Motorcycle data saved locally.")
    except IOError as e:
        print(f"Failed to save data locally: {e}")

def share_motorcycle_data(data):
    """
    Share motorcycle data with a central database.
    """
    try:
        response = requests.post(MOTORCYCLE_DATA_API, json=data)
        if response.status_code == 200:
            print("Motorcycle data shared successfully.")
        else:
            print(f"Error sharing data: {response.status_code}")
    except requests.RequestException as e:
        print(f"Failed to share data: {e}")

def fetch_shared_data(make, model):
    """
    Fetch shared data for a specific make and model.
    """
    try:
        response = requests.get(f"{MOTORCYCLE_DATA_API}?make={make}&model={model}")
        if response.status_code == 200:
            shared_data = response.json()
            print("\nShared data for similar motorcycles:")
            for item in shared_data:
                print(json.dumps(item, indent=4))
            return shared_data
        else:
            print(f"Error fetching shared data: {response.status_code}")
    except requests.RequestException as e:
        print(f"Failed to fetch shared data: {e}")
    return []

# Example Usage
if __name__ == "__main__":
    user_data = collect_motorcycle_data()
    
    # Fetch shared data for the same make and model
    fetch_shared_data(user_data['make'], user_data['model'])

# Initialize GPS
def initialize_system():
    # Start GPS
    gps.configure(on_location=on_gps_update, on_status=on_gps_status)
    gps.start()

    # Ensure gyroscope is working
    if not gyroscope.is_available():
        print("Gyroscope not available!")
        return False

    # Initialize microphone (listener)
    recognizer = sr.Recognizer()
    return recognizer

def on_gps_update(location):
    print(f"Speed: {location['speed']} mp/h")

def on_gps_status(status):
    print(f"GPS status: {status}")

def check_gyroscope():
    gyro_data = gyroscope.rotation
    tilt_angle = abs(gyro_data[1])  # Assuming Y-axis represents tilt
    if tilt_angle > MAX_TILT_ANGLE:
        print(f"Tilt angle too high: {tilt_angle}")
        adjust_motorcycle(tilt_angle)

def adjust_motorcycle(tilt_angle):
    # Logic to adjust motorcycle tilt
    print(f"Adjusting tilt: {tilt_angle}")

def listen_for_accidents(recognizer):
    with sr.Microphone() as source:
        print("Listening for accidents...")
        try:
            audio = recognizer.listen(source, timeout=5)
            loudness = recognize_impact(audio)
            if loudness > THRESHOLD_IMPACT_SOUND:
                report_accident()
        except sr.WaitTimeoutError:
            pass

def report_accident(location):
    """
    Report an accident to emergency services.
    """
    print("Accident detected! Reporting to emergency services...")

    # Prepare payload
    payload = {
        "location": {
            "latitude": location['latitude'],
            "longitude": location['longitude']
        },
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "message": "Accident detected. Immediate assistance required."
    }

    try:
        # Send data to emergency API
        response = requests.post(EMERGENCY_API_URL, json=payload)
        if response.status_code == 200:
            print("Emergency reported successfully.")
        else:
            print(f"Error reporting emergency: {response.status_code}")
    except requests.RequestException as e:
        print(f"Failed to report emergency: {e}")

    # Optionally, send SMS using Twilio
    send_sms_alert(payload)

def send_sms_alert(payload):
    """
    Send an SMS alert with accident details using Twilio.
    """
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Emergency! Accident detected at {payload['location']['latitude']}, {payload['location']['longitude']}. Immediate assistance required.",
            from_=TWILIO_PHONE_NUMBER,
            to=EMERGENCY_CONTACT
        )
        print(f"SMS sent: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")

def recognize_impact(audio):
    # Placeholder: Analyze audio for impact sounds
    return 0  # Replace with actual loudness detection

def report_accident():
    print("Accident detected! Reporting to emergency services...")
    payload = {
        "location": gps.get_location(),
        "timestamp": time.time(),
    }
    try:
        response = requests.post(EMERGENCY_API_URL, json=payload)
        print(f"Emergency reported: {response.status_code}")
    except requests.RequestException as e:
        print(f"Failed to report emergency: {e}")

def main():
    recognizer = initialize_system()
    if not recognizer:
        return

    try:
        while True:
            check_gyroscope()
            listen_for_accidents(recognizer)
            time.sleep(1)
    except KeyboardInterrupt:
        print("System shut down.")

if __name__ == "__main__":
    main()

title = Motorcycle-Accident-Detection
package.name = motorcycle_app
package.domain = com.example

# Version of your application
version = 1.0.0

# (list) Application requirements
requirements = python3, kivy, plyer, requests, twilio

# The entry point of your application
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# (str) Supported orientation (one of: landscape, portrait, all)
orientation = portrait

# (list) Permissions required for the app
android.permissions = INTERNET, ACCESS_FINE_LOCATION, SEND_SMS, RECORD_AUDIO

# (str) Package name (e.g., com.mycompany.myapp)
package.name = motorcycle_app

# (str) Full name of the app (e.g., My Cool App)
title = Motorcycle Accident Detection

# (str) The package domain (e.g., org.mycompany)
package.domain = com.example

# (str) Presplash image
presplash.filename = res/presplash.png

# (str) Icon for the application
icon.filename = res/icon.png

# (list) Supported platforms
# Change to `android` for Android or `ios` for iOS
supported_platforms = android

# (str) Minimum API level for Android
android.minapi = 21

# (str) Target API level for Android
android.api = 33

# (bool) Enable debug mode
debug = True
