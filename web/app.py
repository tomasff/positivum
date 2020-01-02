from flask import Flask
from flask import render_template, abort

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

import datetime

app = Flask('positivum')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/database'

db = SQLAlchemy(app)

association_table = db.Table('articles_sources',
        db.Column('source_id', db.Integer, db.ForeignKey('sources.id')),
        db.Column('article_id', db.Integer, db.ForeignKey('articles.id'))
)

class Article(db.Model):
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer,
            primary_key=True,
            nullable=False)

    title = db.Column(db.String(128),
                nullable=False)

    description = db.Column(db.String(256),
                    nullable=False)

    url = db.Column(db.String(256),
                nullable=False)

    classification = db.Column(db.Integer,
                        nullable=False)

    pub_date = db.Column(db.DateTime, nullable=False)

class Source(db.Model):
    __tablename__ = 'sources'

    id = db.Column(db.Integer,
            primary_key=True,
            nullable=False)

    name = db.Column(db.String(128),
            nullable=False)

    feed_url = db.Column(db.String(256),
                    nullable=False)

    articles = db.relationship('Article', 
                        secondary=association_table,
                        backref='sources')

@app.route('/')
def main():
    articles = db.session.query(Article).filter(Article.classification == 1).order_by(desc(Article.pub_date)).paginate(1, per_page=5)
    return render_template('main.html', articles=articles, title='Positive or neutral', cls=1)

@app.route('/class/<int:cls>')
@app.route('/class/<int:cls>/page/<int:num_page>')
def page(cls = 1, num_page = 1):
    cls_mapping = [
            {'name': 'negative', 'emoji': '😫'},
            {'name': 'positive or neutral', 'emoji': '😊'}
    ]

    try:
        cls_details = cls_mapping[cls]    

        articles = db.session.query(Article).filter(Article.classification == cls).order_by(desc(Article.pub_date)).paginate(num_page, per_page=5)
        title = cls_details['name'].capitalize()

        return render_template('main.html', articles=articles, title=title, cls=cls)
    except IndexError:
        abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error='page not found'), 404

@app.errorhandler(500)
def error_page(e):
    return render_template('error.html', error_code=500, error='an internal error occurred'), 500

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=3000)
