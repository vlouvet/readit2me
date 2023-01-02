import os, wave
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/database/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    isbn = db.Column(db.String, nullable=False)
    cover_image = db.Column(db.LargeBinary)
    page_count = db.Column(db.Integer, nullable=False)

class Recording(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary)
    duration = db.Column(db.Integer)

    def __init__(self, data, duration):
        self.data = data
        self.duration = duration


with app.app_context():    
    # create the database
    db.create_all()

@app.route('/')
def index():
    # retrieve list of books from database
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/recordings')
def recordings():
    recordings = Recording.query.all()
    return render_template('recordings.html', recordings=recordings)


@app.route('/submit_recording', methods=['GET', 'POST'])
def submit_recording():
    books = Book.query.all()
    if request.method == 'POST':
        audio_data = request.files['recording'].read()
        recording = Recording(data=audio_data)
        recording.duration = get_duration(audio_data)
        recording.name = request.form['name']
        # recording.save()
        db.session.add(recording)
        db.session.commit()
        return redirect('/recordings')
    else:
        return render_template('new_recording.html', books=books)

@app.route('/new_book', methods=['GET', 'POST'])
def new_book():
    if request.method == 'POST':
        # retrieve form data
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        page_count = request.form['page_count']
        cover_image = request.files['cover_image']
        cover_image_data = cover_image.read()
        # check if author and title combination already exists
        book = Book.query.filter_by(title=title, author=author).first()
        if book is not None:
            # author and title combination already exists
            flash('A book with the same author and title already exists')
            return redirect(url_for('new_book'))

        # check if ISBN already exists
        book = Book.query.filter_by(isbn=isbn).first()
        if book is not None:
            # ISBN already exists
            flash('A book with the same ISBN already exists')
            return redirect(url_for('new_book'))

        # create and insert new book
        book = Book(title=title, author=author, isbn=isbn, page_count=page_count, cover_image=cover_image_data)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('new_book.html')

@app.route('/books/<int:id>')
def book_details(id):
    # query the Book model by ID
    book = Book.query.get(id)
    if book is None:
        # book not found
        abort(404)
    return render_template('book_details.html', book=book)


def get_duration(wav_file):
    with wave.open(wav_file, 'r') as wav:
        frames = wav.getnframes()
        rate = wav.getframerate()
        duration = frames / float(rate)
        return int(duration * 1000)

def insert_new_book(title, author):
    # code to insert new book into database goes here
    pass

if __name__ == '__main__':
    app.run(port="5001", host="0.0.0.0")
