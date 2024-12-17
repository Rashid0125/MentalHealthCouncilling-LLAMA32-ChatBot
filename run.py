import streamlit as st
from pyngrok import ngrok
import subprocess
import os

# Set your ngrok auth token
ngrok.set_auth_token("2j2cdiWUxqPhlhRff7BKWm7ExuG_5VkGJ3s9bZ66KVGAS2XFn")  # Replace with your actual token

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