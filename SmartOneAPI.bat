@echo off

.\env\Scripts\activate  REM Activate the virtual environment

.\ngrok config add-authtoken 2aSJBJDW6zxjs5wsnKeVVBi12wP_4z5tTvZk5XTHtT4joRgix REM
start cmd /k .\ngrok http --domain=magnetic-eminent-bass.ngrok-free.app 80
start cmd /k python manage.py runserver 80

deactivate  REM 
taskkill /f /im ngrok.exe