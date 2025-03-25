from app import app

from datetime import datetime

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()} 

if __name__ == "__main__":
    app.run() 