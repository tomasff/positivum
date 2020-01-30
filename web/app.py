import os
import datetime

from flask import Flask
from flask import render_template, abort

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, and_

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
    return render_template('articles.html', articles=articles, title='Home', cls=1)

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

        return render_template('articles.html', articles=articles, title=title, cls=cls)
    except IndexError:
        abort(404)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

def gen_str_date_series(lower, upper, step = 1):
    step = datetime.timedelta(days = step)
    current = lower

    while current != upper:
        yield str(current)
        current += step

def unzip(lst):
    return list(map(lambda item: item[0], lst))

@app.route('/statistics')
def statistics():
    stats = dict()

    day_upper = datetime.date.today()
    day_lower = day_upper - datetime.timedelta(days = 5)

    stats['days'] = [*gen_str_date_series(day_lower, day_upper)]

    print(stats['days'])

    stats['articles_total'] = db.session.query(Article).count()
    stats['positive_neutral_total'] = db.session.query(Article).filter(Article.classification == 1).count()
    stats['negative_total'] = db.session.query(Article).filter(Article.classification == 0).count()

    stats['positive_neutral_days_count'] = db.session.query(db.func.count(Article.pub_date)) \
                                        .filter(and_(Article.classification == 1, Article.pub_date > day_lower)) \
                                        .group_by(db.func.date(Article.pub_date)).all()

    stats['positive_neutral_days_count'] = unzip(stats['positive_neutral_days_count']) 

    stats['negative_days_count'] = db.session.query(db.func.count(Article.pub_date)) \
                                        .filter(and_(Article.classification == 0, Article.pub_date > day_lower)) \
                                        .group_by(db.func.date(Article.pub_date)).all()

    stats['negative_days_count'] = unzip(stats['negative_days_count'])

    stats['sources'] = db.session.query(Source).count()

    return render_template('statistics.html', title='Statistics', stats=stats)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', title='Error 404', error='page not found'), 404

@app.errorhandler(500)
def error_page(e):
    return render_template('error.html', title='Error 500', error='an internal error occurred'), 500

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=3000)
