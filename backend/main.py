from processing import Processer
from database import Database, Base

from apscheduler.schedulers.blocking import BlockingScheduler

def main():
    scheduler = BlockingScheduler()
    database = Database(username = 'username', password = 'password', address = 'localhost', name = 'database')

    # Create tables if they do not exist
    Base.metadata.create_all(database.get_engine())

    processer = Processer(database)
    scheduler.add_job(processer.process, 'interval', minutes=30)
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == '__main__':
    main() 
