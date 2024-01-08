@echo off
.\myenv\scripts\activate && python manage.py runserver 80
.\ngrok config add-authtoken 2aSJBJDW6zxjs5wsnKeVVBi12wP_4z5tTvZk5XTHtT4joRgix
start cmd /k .\ngrok http --domain=magnetic-eminent-bass.ngrok-free.app 80
