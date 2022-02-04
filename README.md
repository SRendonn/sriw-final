## Quick setup

Create a virtual environment
```
py -3 -m venv venv

# Linux/macOS
venv/bin/activate

# Windows
venv\Scripts\activate
```

Install dependencies from requirements.txt
```
pip install -r requirements.txt
```

Run flask app
```
# Linux/macOS
export FLASK_APP=app.py
export FLASK_ENV=development

# Windows Powershell
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"

flask run
```