import subprocess
import time
import os
from threading import Thread

def execute_command(command):
    subprocess.Popen(command, shell=True)

def run_ngrok():
    ngrok_auth_token = "2aSJBJDW6zxjs5wsnKeVVBi12wP_4z5tTvZk5XTHtT4joRgix"
    ngrok_domain = "magnetic-eminent-bass.ngrok-free.app"

    # Configure ngrok with authentication token
    execute_command(f".\\ngrok config add-authtoken {ngrok_auth_token}")

    # Run ngrok to expose the local server on port 80
    ngrok_command = f".\\ngrok http --domain={ngrok_domain} 80"
    execute_command(ngrok_command)

def run_django_server():
    django_server_command = "python manage.py runserver 80"
    execute_command(django_server_command)

if __name__ == "__main__":
    # Run ngrok in a separate thread
    ngrok_thread = Thread(target=run_ngrok)
    ngrok_thread.start()

    # Wait for a few seconds to allow ngrok to start
    time.sleep(5)

    # Run Django server in a separate thread
    run_django_server()
