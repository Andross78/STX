from app import db


class DicLang(db.Model):

    __tablename__ = 'dic_lang'

    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.String(2))
