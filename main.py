# Import the Flask application class, template rendering function, HTTP request objects, redirections, URL building helper, and flash messaging from flask package
from flask import Flask, render_template, request, redirect, url_for, flash
# Import the SQLAlchemy database ORM wrapper integration for Flask applications
from flask_sqlalchemy import SQLAlchemy
# Import the declarative base helper and modern type annotations mapped_column/Mapped from sqlalchemy.orm library
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# Import common database SQL column types (Integer, String, Float) from sqlalchemy core
from sqlalchemy import Integer, String, Float
# Import database integrity exception types to handle constraints (like unique title clashes)
from sqlalchemy.exc import IntegrityError

# Initialize the core Flask application, passing the current module's name (__name__) to locate static files and templates
app = Flask(__name__)
# Set a secret key configuration to securely sign and encrypt session cookies, which is required for using flash messages
app.config['SECRET_KEY'] = 'f74a98b1e4274bc7bd1fdf3b05f23efc8192a832049e7552'

# Set the SQLAlchemy database connection URI. "sqlite:///books.db" specifies using a local SQLite database file named 'books.db'
# By default, Flask-SQLAlchemy puts this inside the application's 'instance' folder
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"


# Define a custom base class for Declarative Table mappings, inheriting from SQLAlchemy's DeclarativeBase
class Base(DeclarativeBase):
    # Pass since this class serves as the clean object mapping foundation without requiring additional custom logic
    pass


# Instantiate the SQLAlchemy extension object, passing the custom Base class configuration
db = SQLAlchemy(model_class=Base)
# Connect and initialize the Flask application context instance with the SQLAlchemy database manager extension
db.init_app(app)


# Define a database Model class 'Book' mapped to a SQL table in SQLite, inheriting from db.Model
class Book(db.Model):
    # Map the 'id' column as an Integer primary key, which will auto-increment automatically for new records
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Map the 'title' column as a String limited to 250 characters, requiring non-null entries and enforcing uniqueness across rows
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    # Map the 'author' column as a String limited to 250 characters, requiring non-null entries
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    # Map the 'rating' column as a Float type, representing the rating score, requiring non-null entries
    rating: Mapped[float] = mapped_column(Float, nullable=False)


# Initialize and generate all database tables using the Flask application context block
with app.app_context():
    # Call create_all() to build the tables in SQLite if they don't already exist in the books.db file
    db.create_all()


# Define the index route mapping to the homepage of the library app, supporting GET requests by default
@app.route('/')
def home():
    # Query database and load rows from the Book table, ordering alphabetically by book title
    result = db.session.execute(db.select(Book).order_by(Book.title))
    # Extract mapped Book objects from standard query results using scalars() and fetch all as a list
    all_books = result.scalars().all()
    # Render and return index.html template, supplying the fetched books list to the Jinja rendering engine
    return render_template("index.html", books=all_books)


# Define the add route mapping, supporting both GET (rendering the form) and POST (submitting form inputs)
@app.route("/add", methods=["GET", "POST"])
def add():
    # Process code block if request method matches POST (i.e. user submitted the add form)
    if request.method == "POST":
        # Extract title input from POST request data, stripping potential leading/trailing whitespaces
        title = request.form.get("title", "").strip()
        # Extract author input from POST request data, stripping potential leading/trailing whitespaces
        author = request.form.get("author", "").strip()
        # Extract rating input from POST request data, stripping potential leading/trailing whitespaces
        rating_str = request.form.get("rating", "").strip()

        # Validate that the title input is not empty
        if not title:
            # Flash a warning to the user indicating title cannot be empty
            flash("Book title cannot be empty.", "error")
            # Re-render the add template to let the user fix the empty title input
            return render_template("add.html")

        # Validate that the author input is not empty
        if not author:
            # Flash a warning to the user indicating author cannot be empty
            flash("Author name cannot be empty.", "error")
            # Re-render the add template to let the user fix the empty author input
            return render_template("add.html")

        # Attempt to validate and cast the rating input to a float number
        try:
            # Cast rating string to a float variable
            rating = float(rating_str)
            # Ensure the rating value falls strictly between 0 and 10 bounds inclusive
            if rating < 0 or rating > 10:
                # Raise a value error to invoke the exception handler block if limits are breached
                raise ValueError("Rating must be between 0 and 10.")
        # Handle exceptions if rating is not numeric or breaches defined limits
        except ValueError:
            # Flash a warning to the user indicating the rating is invalid
            flash("Rating must be a valid number between 0.0 and 10.0.", "error")
            # Re-render the add template to let the user fix the rating input
            return render_template("add.html")

        # Instantiate a new Book object mapping inputs to database columns
        new_book = Book(
            title=title,
            author=author,
            rating=rating
        )

        # Start a database transaction block to safely catch integrity issues
        try:
            # Add the new book instance to the current database session unit of work
            db.session.add(new_book)
            # Commit changes to write and save the record to SQLite books.db
            db.session.commit()
            # Flash a success message to confirm the book has been added successfully
            flash(f'"{title}" was successfully added to your library!', "success")
            # Redirect user back to home route after successful addition
            return redirect(url_for('home'))
        # Catch duplicate constraint issues (e.g. title already exists in unique book column)
        except IntegrityError:
            # Rollback database session to reset transaction state after failure
            db.session.rollback()
            # Flash error indicating title duplication
            flash(f'A book with the title "{title}" already exists in your bookshelf.', "error")
            # Re-render the add template to let the user fix the name conflict
            return render_template("add.html")

    # Render and return add.html form template on GET requests
    return render_template("add.html")


# Define the edit route mapping, supporting both GET (loading edit layout) and POST (updating rating score)
@app.route("/edit", methods=["GET", "POST"])
def edit():
    # Process code block if request method matches POST (i.e. user submitted rating changes)
    if request.method == "POST":
        # Extract book ID parameter from form data
        book_id = request.form.get("id")
        # Extract new rating parameter from form data
        rating_str = request.form.get("rating", "").strip()

        # Query and load matching Book record by ID, raising an automatic 404 HTTP page if book not found
        book_to_update = db.get_or_404(Book, book_id)

        # Attempt to validate and cast the edited rating input to a float number
        try:
            # Convert rating string to a float variable
            rating = float(rating_str)
            # Ensure the rating value falls strictly between 0 and 10 bounds inclusive
            if rating < 0 or rating > 10:
                # Raise a value error to invoke the exception handler block if bounds are breached
                raise ValueError("Rating must be between 0 and 10.")
        # Handle exceptions if updated rating is invalid
        except ValueError:
            # Flash warning to the user indicating incorrect input format
            flash("Rating must be a valid number between 0.0 and 10.0.", "error")
            # Re-render edit_rating.html passing the active book instance back for correction
            return render_template("edit_rating.html", book=book_to_update)

        # Update the target book record rating property with validated float score
        book_to_update.rating = rating
        # Commit changes to save updated rating in books.db
        db.session.commit()
        # Flash success feedback confirming the rating has updated successfully
        flash(f'Rating for "{book_to_update.title}" updated successfully to {rating}/10.', "success")
        # Redirect user back to library index home page
        return redirect(url_for('home'))

    # Load book record on GET request by retrieving the 'id' parameter from request URL query string
    book_id = request.args.get('id')
    # Retrieve matching book object by primary key ID or return a 404 if invalid ID passed
    book_selected = db.get_or_404(Book, book_id)
    # Render and return edit_rating.html template, supplying loaded book details to pre-populate elements
    return render_template("edit_rating.html", book=book_selected)


# Define the delete route mapping to remove records via URL parameter routing
@app.route("/delete")
def delete():
    # Retrieve book ID parameter from request URL query string arguments
    book_id = request.args.get('id')

    # Query and fetch corresponding book record by primary key ID, raising a 404 if not found
    book_to_delete = db.get_or_404(Book, book_id)
    # Queue target book object for deletion in database transaction session
    db.session.delete(book_to_delete)
    # Commit transaction to execute SQL DELETE statement in books.db file
    db.session.commit()
    # Flash success message verifying book deletion
    flash(f'"{book_to_delete.title}" was successfully deleted from your library.', "success")
    # Redirect user back to home route catalog page
    return redirect(url_for('home'))


# Check if file execution occurs directly in command terminal instead of import modules
if __name__ == "__main__":
    # Start and run the local development server with debug mode enabled to auto-restart on changes
    app.run(debug=True)
