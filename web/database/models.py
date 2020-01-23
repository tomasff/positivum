from . import db

articles_sources = db.Table('articles_sources',
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
                        secondary=articles_sources,
                        backref='sources')

