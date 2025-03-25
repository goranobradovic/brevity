# Brevity

A Python-based micro-blog engine that renders markdown content to HTML and stores content in a MySQL database.

## Features

- Markdown to HTML rendering
- MySQL-based storage
- User authentication
- Simple and clean UI
- Post creation, editing, and deletion

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/brevity.git
cd brevity
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```
FLASK_APP=brevity
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URI=mysql://username:password@localhost/brevity
```

5. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Run the application:
```bash
flask run
```

## Usage

1. Visit `http://localhost:5000` in your browser
2. Register a new account
3. Create, edit, and delete posts using markdown formatting

## License

This project is licensed under the terms of the LICENSE file included. 