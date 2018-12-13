from app import app
from flask_sqlalchemy import SQLAlchemy
import os
import time

file_path = os.path.abspath(os.getcwd())+"\\test_database.db"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)

class FinishedUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    time = db.Column(db.String(120), unique=False, nullable=True)
    mistakes = db.Column(db.String(120), unique=False, nullable=True)
    creationDate = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return '<FinishedUser %r %r %r %r>' % (self.username, self.time, self.mistakes, self.creationDate)

class LiveUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    currentDoc = db.Column(db.String(120), unique=False, nullable=True)
    totalDocs = db.Column(db.String(120), unique=False, nullable=True)
    creationDate = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return '<LiveUser %r %r %r %r>' % (self.username, self.currentDoc, self.totalDocs, self.creationDate)


def db_add_finished_user(username, time, mistakes, creationDate):
    user = FinishedUser(username=username, time=time, mistakes=mistakes, creationDate=creationDate)
    db.session.add(user)
    db.session.commit()
    
def db_add_live_user(username, currentDoc, totalDocs, creationDate):
    user = LiveUser(username=username, currentDoc=currentDoc, totalDocs=totalDocs, creationDate=creationDate)
    db.session.add(user)
    db.session.commit()


def db_add_live_player(incoming_live_player):
    creationDate = str(int(time.mktime(time.localtime())))
    db_add_live_user(username=incoming_live_player['username'],
                     currentDoc=incoming_live_player['current_doc'], totalDocs=incoming_live_player['total_docs'], creationDate=creationDate)

def db_add_finishing_player(incoming_finishing_player):
    creationDate = db_get_live_user_creation_date(incoming_finishing_player['username'])
    db_add_finished_user(username=incoming_finishing_player['username'], time=incoming_finishing_player['time'], 
                     mistakes=incoming_finishing_player['mistakes'], creationDate=creationDate)
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

def db_get_live_user_creation_date(username):
    live_user = LiveUser.query.filter(LiveUser.username == username).first()
    if live_user is not None:
        return live_user.creationDate
    return None

def db_user_has_finished(username):
    return FinishedUser.query.filter(FinishedUser.username == username).first() is not None

def db_user_get_finished_user(username):
    return FinishedUser.query.filter(FinishedUser.username == username).first()

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
        live_users.append({'username':live_user.username,'current_doc':live_user.currentDoc, 'total_docs':live_user.totalDocs, 'creation_date':live_user.creationDate})
    return live_users

def db_get_all_finished_users_as_list():
    query_entries = db.session.query(FinishedUser).order_by(FinishedUser.mistakes).order_by(FinishedUser.time).all()
    # print query_entries
    finished_users = []
    for finished_player in query_entries:
        finished_users.append({'username':finished_player.username,'time':finished_player.time, 'mistakes':finished_player.mistakes, 'creation_date':finished_player.creationDate})
    return finished_users

def db_get_all_finished_robots_as_list():
    query_entries = db.session.query(FinishedUser).filter(FinishedUser.username.like('mRobot%')).order_by(FinishedUser.mistakes).order_by(FinishedUser.time)
    # print query_entries
    finished_robots = []
    for finished_player in query_entries:
        finished_robots.append({'username':finished_player.username,'time':finished_player.time, 'mistakes':finished_player.mistakes})
    return finished_robots

def db_get_all_finished_humans_as_list():
    query_entries = db.session.query(FinishedUser).filter(~FinishedUser.username.like('mRobot%')).order_by(FinishedUser.mistakes).order_by(FinishedUser.time).all()
    # print query_entries
    finished_humans = []
    for finished_player in query_entries:
        robotInfo = db_get_robot_time_from_username(finished_player.username)
        finished_humans.append({'username':finished_player.username,'time':finished_player.time, 'mistakes':finished_player.mistakes, 'robot_time':robotInfo[0], 'robot_mistakes':robotInfo[1]})
    return finished_humans

def db_get_robot_time_from_username(username):
    human_user = db_user_get_finished_user(username) if db_user_has_finished(username) else None
    human_creation_date = human_user.creationDate
    # print "human creation date ="+human_creation_date
    robot_list = db_get_all_finished_robots_as_list()
    # print "robot list ="+str(robot_list)
    for robot in robot_list:
        if human_creation_date in robot['username']:
            return [robot['time'], robot['mistakes']]
    return ['NA','NA']
