from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from contextlib import contextmanager

class Database:
    def __init__(self, username: str , password: str, address: str, name: str):
        self.uri = 'mysql+pymysql://{:s}:{:s}@{:s}/{:s}'.format(username, password, address, name)
        self.engine = create_engine(self.uri)
        self.Session = sessionmaker(bind=self.engine)

    def get_engine(self):
        return self.engine

    @contextmanager
    def get_session(self):
        session = self.Session()

        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


Base = declarative_base()

association_table = Table('articles_sources', Base.metadata,
        Column('source_id', Integer, ForeignKey('sources.id')),
        Column('article_id', Integer, ForeignKey('articles.id'))
)

class Article(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer,
            primary_key=True,
            nullable=False)

    title = Column(String(128),
                nullable=False)

    description = Column(String(256),
                    nullable=False)

    url = Column(String(256),
                nullable=False)

    classification = Column(Integer,
                        nullable=False)

    # UTC
    pub_date = Column(DateTime, nullable=False)


class Source(Base):
    __tablename__ = 'sources'

    id = Column(Integer,
            primary_key=True,
            nullable=False)

    name = Column(String(128),
            nullable=False)

    feed_url = Column(String(256),
                    nullable=False)

    articles = relationship('Article', 
                        secondary=association_table,
                        backref='sources')


