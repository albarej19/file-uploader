# File Upload Project! 

This is a Python project - a file management system I built while using FastAPI. Here's how to use it:

## What does this do?
This is a simple file upload system where you can:
- Upload files
- Save them
- Get info about your uploads
- Store file data in a SQLite database
- Handle multiple uploads without file name conflicts

## How to set it up on your computer

### Stuff you need first:
- Python (Used version 3.8)
- Git (to clone the project)

### Steps to get it running:

1. First, get the code:
```
git clone [put your repo url here]
cd [your folder name]
```

2. Make a virtual environment:
```
# Make a new environment
python3 -m venv venv

# Turn it on - For Windows:
.\venv\Scripts\activate

# For Mac/Linux users:
source venv/bin/activate
```

3. Install the packages we need:
```
pip install -r requirements.txt
```

Here's what you need in your requirements.txt file:
- fastapi
- uvicorn
- sqlalchemy
- pydantic
- python-multipart

4. Set up the database:
The nice thing about this project is that it uses SQLite, so you don't need to install any special database! The database file (`file_data.db`) will be created automatically when you first run the app. The tables will be created based on the models in `models.py` - pretty neat, right?

5. Start the server:
```
uvicorn main:app --reload
```

That's it! The server should be running at http://127.0.0.1:8000 
You can see the API docs at http://127.0.0.1:8000/docs

## How I built this �

### Why I organized the files this way:
I tried to keep things organized by splitting the code into different files:

- `main.py` - This is where everything starts! It has all the routes and API endpoints. I put them here because it's the first place people look
- `schemas.py` - Handles the data validation (makes sure everything works right). Keeps all the Pydantic models in one place
- `models.py` - Database stuff lives here. All the SQLAlchemy models that create the database tables
- `database.py` - More database stuff (connects to SQLite). Has the database connection setup
- `uploaded_files/` - Where the actual files get saved. I keep this separate so it's easy to find uploaded files

### Things I learned while making this:

1. How to make unique filenames:
I used something called UUID to make sure no two files have the same name - even if users upload files with the same name.

2. How I handle saving files:
- First, save the actual file
- Then save the info about the file in the database
- If something goes wrong with the database, the file still stays saved.

### Problems I ran into

- Accidentally pushed the uploaded_files folder to git
- Fixed it by learning about .gitignore (you live and learn, right?)

### TODO (stuff I want to add later):
- [ ] Maybe add a way to delete files
- [ ] Make it look prettier
- [ ] Add user accounts

That's pretty much it! Feel free to use this code.
