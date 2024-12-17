import streamlit as st
from pyngrok import ngrok
import subprocess
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the auth_key
auth_key = os.getenv("ngrok_key")

# Set your ngrok auth token
ngrok.set_auth_token(auth_key)  # Replace with your actual token

# Get the dev server port (defaults to 8501)
port = 8501

# Open a ngrok tunnel to the dev server
public_url = ngrok.connect(port).public_url
print(f"Public URL: {public_url}")

# Update the environment variable for Streamlit to use
os.environ['STREAMLIT_SERVER_PORT'] = str(port)

# Run the Streamlit app
print("Running Streamlit app...")
subprocess.Popen(['streamlit', 'run', 'app.py'])

# Keep the notebook running
import time
while True:
    time.sleep(1)