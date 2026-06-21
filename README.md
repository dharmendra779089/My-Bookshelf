# 📚 My Bookshelf

My Bookshelf is a premium, lightweight personal library cataloging web application. Built using Python, Flask, Flask-SQLAlchemy, SQLite, and vanilla CSS, it allows users to track their read books, manage authors, log custom ratings (0.0 to 10.0), and maintain a clean digital inventory.

The application has been enhanced with a stunning **modern glassmorphism dark-mode UI**, complete form validation (client-side and server-side), transactional integrity handlers for duplicate prevention, dynamic flash alerts, and comprehensive inline code documentation.

---

## ✨ Features

*   **Sleek Glassmorphic Design**: A premium responsive interface styled with custom HSL variable color systems, translucent frosted-glass panels (`backdrop-filter`), typography systems (Google Fonts Inter), and custom-bezier micro-animations.
*   **Complete CRUD Capabilities**:
    *   **Create**: Add new books with custom titles, author names, and rating values.
    *   **Read**: Displays all catalog entries dynamically, sorted alphabetically by title.
    *   **Update**: Modify ratings seamlessly via clean edit controls.
    *   **Delete**: Safely remove catalog entries with interactive confirmation prompt overlays.
*   **Robust Input Sanitization & Validation**:
    *   Strips accidental whitespaces from text inputs automatically.
    *   Rejects empty values (Title & Author) gracefully, prompting user feedback.
    *   Validates numeric rating parameters strictly between `0.0` and `10.0` (both via HTML5 number parameters on the frontend and Float casting validation on the backend).
*   **Transactional Integrity Error Handling**: Intercepts SQLite unique constraints. If a duplicate book title is added, the app rolls back database sessions safely, notifies the user with a warning banner, and prevents crashes.
*   **Dynamic Flash Notifications**: Generates styled context alerts for successes (add, update, delete) and validation errors.
*   **SEO Optimized**: Semantic HTML5 markup layout structures and responsive mobile scaling configurations.

---

## 🛠️ Tech Stack

*   **Backend Framework**: Flask (Python)
*   **Database Management**: SQLite
*   **ORM Layer**: Flask-SQLAlchemy (SQLAlchemy 2.0 declarative system)
*   **Frontend Templating**: Jinja2 (HTML5)
*   **Styling Engine**: Vanilla CSS (CSS3 variables, transitions, and flexbox/grid)

---

## 📂 Project Structure

```text
My Bookshelf/
│
├── instance/
│   └── books.db             # Local SQLite database file (created automatically)
│
├── static/
│   └── css/
│       └── style.css        # Premium Vanilla CSS stylesheet system
│
├── templates/
│   ├── index.html           # Library catalog dashboard
│   ├── add.html             # Add new book form page
│   └── edit_rating.html     # Edit book rating form page
│
├── main.py                  # Core Flask router, DB model configurations, and controller logic
├── requirements.txt         # Project package dependencies
└── README.md                # Project documentation
```

---

## 🚀 Setup & Installation

Follow these steps to run the application locally on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/my-bookshelf.git
cd my-bookshelf
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python main.py
```

Once running, the terminal will indicate that the application is serving on:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

Open the link in your web browser to explore your bookshelf.

---

## 🔄 Core Workflows

### 📖 Read (Homepage)
*   Routes to `/`.
*   Retrieves all records from the SQLite database using:
    `db.session.execute(db.select(Book).order_by(Book.title)).scalars().all()`
*   Renders list items inside responsive grid card blocks. If the library database contains no entries, it renders a custom empty-state placeholder block.

### ➕ Create (Add Book)
*   Routes to `/add` (supporting `GET` and `POST`).
*   Runs backend validation to prevent empty title/author inputs and checks that ratings fall between `0.0` and `10.0`.
*   Checks if the title already exists. If yes, it triggers an `IntegrityError` catch-block, rollbacks the transaction (`db.session.rollback()`), and flashes an error warning. Otherwise, it commits the changes and redirects to the homepage.

### ✏️ Update (Modify Rating)
*   Routes to `/edit` (supporting `GET` and `POST`).
*   Retrieves the selected database record dynamically by primary ID: `db.get_or_404(Book, book_id)`.
*   Modifies the rating value, commits the update, flashes a success notification banner, and redirects home.

### ❌ Delete (Remove Book)
*   Routes to `/delete` (supporting `GET`).
*   Prompts a confirmation window to prevent accidental clicks.
*   Finds the book object by URL ID argument, calls `db.session.delete()`, commits the change, and redirects to the index view.

---

## 🔒 Security & Best Practices

*   **Session Security**: Set up with a local cryptographically secure `SECRET_KEY` config to handle cookie signing.
*   **Database Isolation**: SQLite context connections are run within Flask's application context (`app.app_context()`) to safeguard model structures.
*   **Sanitization**: User inputs are stripped of trailing spaces to keep table attributes uniform.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
