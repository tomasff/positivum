import os
import datetime

from flask import Flask
from flask import render_template, abort

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from database import db
from database.models import Article, Source

app = Flask('positivum')

app.config['ARTICLES_PER_PAGE'] = os.getenv('ARTICLES_PER_PAGE', 10)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
                    os.getenv('DATABASE_USERNAME'),
                    os.getenv('DATABASE_PASSWORD'), 
                    os.getenv('DATABASE_HOSTNAME'), 
                    os.getenv('DATABASE_NAME'))  

db.init_app(app)

@app.route('/')
def main():
    articles = db.session.query(Article).filter(Article.classification == 1).order_by(desc(Article.pub_date)).paginate(1, per_page=app.config['ARTICLES_PER_PAGE'])
    return render_template('main.html', articles=articles, title='Home', cls=1)

@app.route('/class/<int:cls>')
@app.route('/class/<int:cls>/page/<int:num_page>')
def page(cls = 1, num_page = 1):
    cls_mapping = [
            {'name': 'negative', 'emoji': '😫'},
            {'name': 'positive or neutral', 'emoji': '😊'}
    ]

    try:
        cls_details = cls_mapping[cls]    

        articles = db.session.query(Article).filter(Article.classification == cls).order_by(desc(Article.pub_date)).paginate(num_page, per_page=app.config['ARTICLES_PER_PAGE'])
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
