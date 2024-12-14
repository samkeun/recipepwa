# Netlify deploy
pip install Frozen-Flask

# freeze.py
from flask_frozen import Freezer
from recipe import app

freezer = Freezer(app)

if __name__ == "__main__":
    freezer.freeze()


# Run
python freeze.py


# WSGI 서버 사용
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 recipe:app


