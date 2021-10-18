import traceback

from app import db, session


class Book(db.Model):

    __tablename__ = 'book'

    book = ''

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    author = db.Column(db.String(64))
    publish_date = db.Column(db.DateTime)
    ISBN_num = db.Column(db.String(13))
    pages_count = db.Column(db.Integer)
    preview_link = db.Column(db.String(128))
    lang = db.Column(db.String(2))


    def __repr__(self):
        return f'Book {self.title}'


    def update_book(self, data):

        if session['oper_type'] == 1:
            book = Book()
        else:
            book = Book.query.filter_by(id=session['book_id']).first()
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'publish_date' in data:
            book.publish_date = data['publish_date']
        if 'isbn' in data:
            book.ISBN_num = data['isbn']
        if 'pages_count' in data:
            book.pages_count = data['pages_count']
        if 'preview_link' in data:
            book.preview_link = data['preview_link']
        if 'lang' in data:
            book.lang = data['lang']

        try:
            db.session.add(book)
            db.session.commit()
        except Exception:
            print(traceback.print_exc())

        return book


    def prepare_form(self, book, form):

        form.title.data = book.title
        form.author.data = book.author
        form.publish_date.data = book.publish_date
        form.isbn.data = book.ISBN_num
        form.pages_count.data = book.pages_count
        form.preview_link.data = book.preview_link
        form.lang.data = book.lang

        return form


    def serialize(self):
        output = {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "publish_date": self.publish_date,
            "ISBN_num": self.ISBN_num,
            "pages_count": self.pages_count,
            "preview_link": self.preview_link,
            "lang": self.lang
        }
        return output