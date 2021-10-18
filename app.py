from datetime import datetime
import json
import requests

from flask import (
    Flask,
    request,
    render_template,
    redirect,
    session,
    flash,
    jsonify)
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Oscar-1003@localhost/STXdatabase'

app.config['SECRET_KEY'] = '6ef40ecccd16b865a7e00b6e49d902ea'

db = SQLAlchemy(app)
db.init_app(app)

GOOGLE_URL = 'https://www.googleapis.com/books/v1/volumes?q=Hobbit'


from models.books import Book
from models.dic_lang import DicLang

from forms import BookFrm


@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    Listing all books from db and import books from google api
    '''

    session['book_id'] = 0
    books = Book.query.order_by(Book.id).all()
    form = BookFrm(request.form)

    if request.method == 'POST':
        data = request.form

        if 'google_import' in request.form:
            session['oper_type'] = 1

            response = requests.get(GOOGLE_URL)
            res = json.loads(response.text)
            load_books = res['items']

            for book in load_books:
                new_book_data = {}
                book_data = book['volumeInfo']
                new_book_data['title'] = book_data['title']
                new_book_data['author'] = (', '.join([a for a in book_data['authors']]))
                new_book_data['publish_date'] = book_data['publishedDate']
                new_book_data['isbn'] = book_data['industryIdentifiers'][0]['identifier']
                if 'pageCount' in book_data:
                    new_book_data['pages_count'] = book_data['pageCount']
                new_book_data['preview_link'] = book_data['previewLink']
                new_book_data['lang'] = book_data['language']

                Book.update_book(Book(), new_book_data)

            books = Book.query.order_by(Book.id).all()
            return(render_template(
                'index.html',
                books=books,
                form=form,)
            )

        if 'book_id' in data:
            dic_lang = DicLang.query.all()
            book = Book.query.filter_by(id=data['book_id']).first()
            form = Book.prepare_form(Book(), book, form)
            form.lang.choices = [(d.id, d.lang) for d in dic_lang]
            session['book_id'] = book.id
            session['oper_type'] = 2

            return redirect('/book_details')

        if 'filter_submit' in data:
            value = data['filter_input']
            book_filter = data['filter_type']
            if book_filter == 'title':
                books = Book.query.filter_by(title=value).order_by(Book.id).all()
            elif book_filter == 'author':
                books = Book.query.filter_by(author=value).order_by(Book.id).all()
            elif book_filter == 'lang':
                books = Book.query.filter_by(lang=value).order_by(Book.id).all()
            else:
                second_value = data['second_date_input']
                books = Book.query.filter(Book.publish_date.between(value, second_value))\
                    .order_by(Book.id).all()
            if len(books) == 0:
                books = Book.query.order_by(Book.id).all()
                flash('No books fit your filter')

    return render_template(
        'index.html',
        books=books,
        form=form,
    )


@app.route('/book_details', methods=['GET', 'POST'])
def book_details():
    '''
    Creating new or editing exist book, depends on session['oper_type']
    1 = Create book
    2 = Edit book
    '''


    title = 'New book'
    valid_error = False

    form = BookFrm(request.form)

    dic_lang = DicLang.query.all()
    form.lang.choices = [(d.lang, d.lang) for d in dic_lang]

    session['oper_type'] = 1 if session['book_id'] == 0 else 2

    if session['book_id'] != 0:
        title = 'Book edition'
        book = Book.query.filter_by(id=session['book_id']).first()
        form = Book.prepare_form(Book(), book, form)

    if request.method == "POST":
        data = request.form

        if 'book_save' in data:

            if len(data['title']) >= 32:
                flash('Title can be max 32 chars')
                valid_error = True

            if len(data['author']) >= 128:
                flash('Author can be max 128 chars')
                valid_error = True

            if len(data['isbn']) >= 13:
                flash('ISBN number can be max 13 chars')
                valid_error = True

            if len(data['preview_link']) >= 128:
                flash('Preview link can be max 128 chars')
                valid_error = True

            try:
                datetime.strptime(data['publish_date'], '%Y-%m-%d')
            except ValueError:
                flash('Wrong datatype in "Publish date" field')
                valid_error = True

            try:
                isinstance(int(data['pages_count']), int)
            except ValueError:
                flash('Wrong datatype in "Pages count" field')
                valid_error = True

            if not valid_error:
                Book.update_book(Book(), data)
                return redirect('/')

            return redirect('/book_details')

    return render_template(
        'book_details.html',
        title=title,
        form=form,
    )


@app.route('/api_books', methods=['GET'])
def api_books():
    '''
    Return all books with filters: value, title, lang, publish_date in query string
    '''


    books = Book.query.order_by(Book.id).all()

    if 'filter' in request.args:
        value = request.args['value']
        book_filter = request.args['filter']
        if book_filter == 'title':
            books = Book.query.filter_by(title=value).order_by(Book.id).all()
        elif book_filter == 'author':
            books = Book.query.filter_by(author=value).order_by(Book.id).all()
        elif book_filter == 'lang':
            books = Book.query.filter_by(lang=value).order_by(Book.id).all()
        if book_filter == 'publish_date':
            if 'second_value' in request.args:
                second_value = request.args['second_value']
                books = Book.query.filter(Book.publish_date.between(value, second_value))\
                    .order_by(Book.id).all()
        if len(books) == 0:
            return 'No books fit your filter'

    output = [Book.serialize(book) for book in books]
    response = {}
    response['data'] = output
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
