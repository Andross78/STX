from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    IntegerField,
    DateField,
)

from wtforms.validators import DataRequired


class BookFrm(FlaskForm):
    title = StringField('Title',
        render_kw={"class":"col-8"},
        validators=[DataRequired()])
    author = StringField('Author',
        render_kw={"class":"col-8"},
        validators=[DataRequired()])
    publish_date = StringField('Publish date',
        render_kw={"placeholder": "YYYY-MM-DD", "class":"col-8"},
        validators=[DataRequired()])
    isbn = StringField('ISBN number',
        render_kw={"class":"col-8"},
        validators=[DataRequired()])
    pages_count = IntegerField('Pages count',
        render_kw={"class": "col-8"},
        validators=[DataRequired()])
    preview_link = StringField('Preview link',
        render_kw={"class":"col-8"},
        validators=[DataRequired()])
    lang = SelectField('Language',
        render_kw={"class":'text-uppercase mr-5'})