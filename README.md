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
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
# Use SQLite (easier setup)
DATABASE_URI=sqlite:///brevity.db
# Or use MySQL
# DATABASE_URI=mysql://username:password@localhost/brevity
```

5. Set up the database:
   - If using SQLite, the database file will be created automatically
   - If using MySQL, create a database named `brevity` first
   
   Then run the initialization script to create tables and sample data:
   ```bash
   python init_db.py
   ```

   Or use Flask-Migrate to initialize the database:
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
2. Log in with the default admin account:
   - Username: `admin`
   - Password: `adminpassword` (you should change this immediately!)
3. Create, edit, and delete posts using markdown formatting

## Project Structure

- `app.py` - Main Flask application
- `models.py` - Database models (User, Post, Settings)
- `routes/` - Application routes organized by function
  - `main.py` - Main routes (index, about)
  - `auth.py` - Authentication routes (login, register, profile)
  - `posts.py` - Post management routes (create, edit, delete, view)
- `templates/` - HTML templates
- `static/` - Static assets (CSS, etc.)

## License

This project is licensed under the terms of the LICENSE file included. 