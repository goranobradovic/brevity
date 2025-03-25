"""
Run script for Brevity blog
"""
import os
import sys
from datetime import datetime

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app

app = create_app()

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()} 

if __name__ == '__main__':
    app.run(debug=True) 