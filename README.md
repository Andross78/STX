# STX

App is hosted on heroku : https://vast-cove-96774.herokuapp.com/

For running this projects you have to clone this repo:
git clone https://github.com/Andross78/STX.git

install all modules:
pip install -r req.txt

and run:
flask run

Views:

1. '/' All books listing
2. '/book_details' Create or update book (depends on session['oper_type'])
3. '/api_books' Get all books api with filters in query string: ('title', 'author', 'lang', 'publish_date') and 'value'. If fiter == 'publish_date', adding 'second_value' in query string is obligatory.
