from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
import random

app = Flask(__name__, static_folder='static', template_folder='templates')

# --- Configuration ---
# Define the path to your JSON file within the static folder
# It's important to put it in 'static' if you want client-side JavaScript to potentially fetch it directly
# for initial loads, but for writing, the server must handle it.
JSON_FILE_PATH = os.path.join(app.root_path, 'static', 'bible_verses.json')

# --- Helper Functions for JSON File Handling ---
def load_bible_verses():
    """Loads all Bible verses from the JSON file."""
    if os.path.exists(JSON_FILE_PATH):
        try:
            with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
                # Ensure the file is not empty before trying to load JSON
                content = f.read()
                if content:
                    return json.loads(content)
                return [] # Return empty list if file is empty
        except json.JSONDecodeError:
            # Handle cases where the JSON file is corrupted or malformed
            print(f"Warning: JSON file at {JSON_FILE_PATH} is empty or invalid. Starting with empty list.")
            return []
    return [] # Return empty list if file does not exist

def save_bible_verses(verses):
    """Saves the current list of Bible verses to the JSON file."""
    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(verses, f, indent=2, ensure_ascii=False) # indent for readability

# --- Initialize or Load Verses on App Startup ---
# This list will hold all verses in memory for quick access
all_bible_verses = load_bible_verses()

# If the JSON file was empty or didn't exist, populate it with initial data
if not all_bible_verses:
    initial_verses = [
        {"text": "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.", "reference": "John 3:16"},
        {"text": "I can do all this through him who gives me strength.", "reference": "Philippians 4:13"},
        {"text": "Trust in the LORD with all your heart and lean not on your own understanding; in all your ways submit to him, and he will make your paths straight.", "reference": "Proverbs 3:5-6"},
        {"text": "The LORD is my shepherd, I lack nothing. He makes me lie down in green pastures, he leads me beside quiet waters, he refreshes my soul.", "reference": "Psalm 23:1-3"},
        {"text": "Be strong and courageous. Do not be afraid; do not be discouraged, for the LORD your God will be with you wherever you go.", "reference": "Joshua 1:9"},
        {"text": "But those who hope in the LORD will renew their strength. They will soar on wings like eagles; they will run and not grow weary, they will walk and not be faint.", "reference": "Isaiah 40:31"},
        {"text": "For I know the plans I have for you, declares the LORD, plans to prosper you and not to harm you, plans to give you hope and a future.", "reference": "Jeremiah 29:11"},
        {"text": "And we know that in all things God works for the good of those who love him, who have been called according to his purpose.", "reference": "Romans 8:28"},
        {"text": "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God.", "reference": "Philippians 4:6"},
        {"text": "Therefore I tell you, whatever you ask for in prayer, believe that you have received it, and it will be yours.", "reference": "Mark 11:24"},
        {"text": "The name of the LORD is a fortified tower; the righteous run to it and are safe.", "reference": "Proverbs 18:10"},
        {"text": "But seek first his kingdom and his righteousness, and all these things will be given to you as well.", "reference": "Matthew 6:33"},
        {"text": "Come to me, all you who are weary and burdened, and I will give you rest.", "reference": "Matthew 11:28"},
        {"text": "Be kind and compassionate to one another, forgiving each other, just as in Christ God forgave you.", "reference": "Ephesians 4:32"},
        {"text": "Let us not become weary in doing good, for at the proper time we will reap a harvest if we do not give up.", "reference": "Galatians 6:9"}
    ]
    save_bible_verses(initial_verses)
    all_bible_verses = initial_verses # Update the in-memory list

# --- Routes ---

@app.route('/')
def index():
    """Renders the main home page."""
    return render_template('index.html')

@app.route('/upload')
def upload_page():
    """Renders the verse upload page."""
    return render_template('upload.html')

@app.route('/submit_verse', methods=['POST'])
def submit_verse():
    """Handles the form submission from the upload page."""
    book = request.form.get('book')
    chapter = request.form.get('chapter')
    verse_num = request.form.get('verse')
    content = request.form.get('content')

    if not all([book, chapter, verse_num, content]):
        # You might want to show an error message on the upload page
        return "Missing data!", 400

    # Format the new verse as expected by your display script
    new_verse = {
        "text": content,
        "reference": f"{book} {chapter}:{verse_num}"
    }

    global all_bible_verses # Indicate we are modifying the global list
    all_bible_verses.append(new_verse)
    save_bible_verses(all_bible_verses) # Save the updated list to the JSON file

    # Redirect back to the upload page or a success page
    return redirect(url_for('upload_page', message="Verse uploaded successfully!"))

@app.route('/get_random_verse')
def get_random_verse():
    """API endpoint to provide a random Bible verse as JSON."""
    if not all_bible_verses:
        return jsonify({"text": "No verses available.", "reference": ""}), 200
    
    verse = random.choice(all_bible_verses)
    return jsonify(verse)

if __name__ == '__main__':
    app.run(debug=True) # Run in debug mode for development