from app import app
from flask_sqlalchemy import SQLAlchemy
import os


file_path = os.path.abspath(os.getcwd())+"\\test_database.db"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)

class FinishedUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    time = db.Column(db.String(120), unique=False, nullable=True)
    mistakes = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return '<FinishedUser %r %r %r>' % (self.username, self.time, self.mistakes)

class LiveUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    currentDoc = db.Column(db.String(120), unique=False, nullable=True)
    totalDocs = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return '<LiveUser %r %r %r>' % (self.username, self.currentDoc, self.totalDocs)


def db_add_finished_user(username, time, mistakes):
    user = FinishedUser(username=username, time=time, mistakes=mistakes)
    db.session.add(user)
    db.session.commit()
    
def db_add_live_user(username, currentDoc, totalDocs):
    user = LiveUser(username=username, currentDoc=currentDoc, totalDocs=totalDocs)
    db.session.add(user)
    db.session.commit()


def db_add_live_player(incoming_live_player):
    db_add_live_user(username=incoming_live_player['username'],
                     currentDoc=incoming_live_player['current_doc'], totalDocs=incoming_live_player['total_docs'])

def db_add_finishing_player(incoming_finishing_player):
    db_add_finished_user(username=incoming_finishing_player['username'], time=incoming_finishing_player['time'], 
                     mistakes=incoming_finishing_player['mistakes'])
    print "player finishing, remove it from the live db"
    db_rm_live_player(incoming_finishing_player['username'])
        
def db_rm_live_player(username):
    if (db_user_is_live(username)):
        user = LiveUser.query.filter(LiveUser.username == username).first()
        db.session.delete(user)
        db.session.commit() 

def db_user_is_live(username):
    print "db_user_exists?"+ str(LiveUser.query.filter(LiveUser.username == username).first() is not None)
    return LiveUser.query.filter(LiveUser.username == username).first() is not None

def db_user_has_finished(username):
    print "db_user_has_finished?"+ str(FinishedUser.query.filter(FinishedUser.username == username)).first() is not None
    return FinishedUser.query.filter(FinishedUser.username == username).first() is not None

def db_user_update_live_player(incoming_live_player):
    username = incoming_live_player['username']
    # Does it exist already?
    if db_user_is_live(username):
        user = LiveUser.query.filter(LiveUser.username == username).first()
        print "User = "+ str(user)
        user.currentDoc = incoming_live_player['current_doc']
        user.totalDocs = incoming_live_player['total_docs']
        db.session.commit()
    else:
        print "User doesn't exist, create it"
        db_add_live_player(incoming_live_player)

def db_get_all_live_users_as_list():
    query_entries = LiveUser.query.all()
    live_users = []
    for live_user in query_entries:
        live_users.append({'username':live_user.username,'current_doc':live_user.currentDoc, 'total_docs':live_user.totalDocs})
    return live_users

def db_get_all_finished_users_as_list():
    query_entries = db.session.query(FinishedUser).order_by(FinishedUser.mistakes).order_by(FinishedUser.time).all()
    # print query_entries
    finished_users = []
    for finished_player in query_entries:
        finished_users.append({'username':finished_player.username,'time':finished_player.time, 'mistakes':finished_player.mistakes})
    return finished_users

def db_get_all_finished_robots_as_list():
    query_entries = db.session.query(FinishedUser).filter(FinishedUser.username.like('Robo%')).order_by(FinishedUser.mistakes).order_by(FinishedUser.time)
    # print query_entries
    finished_robots = []
    for finished_player in query_entries:
        finished_robots.append({'username':finished_player.username,'time':finished_player.time, 'mistakes':finished_player.mistakes})
    return finished_robots

def db_get_all_finished_humans_as_list():
    query_entries = db.session.query(FinishedUser).filter(~FinishedUser.username.like('Robo%')).order_by(FinishedUser.mistakes).order_by(FinishedUser.time).all()
    # print query_entries
    finished_humans = []
    for finished_player in query_entries:
        finished_humans.append({'username':finished_player.username,'time':finished_player.time, 'mistakes':finished_player.mistakes})
    return finished_humans
