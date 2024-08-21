from . import db,admin
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import jsonify
from sqlalchemy import inspect
import datetime
import calendar
from sqlalchemy.sql import func
import pytz


class User(UserMixin, db.Model):
    id=db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True, unique=True)
    #email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #recipes = db.relationship('Recipe', backref='author', lazy = 'dynamic')
    checkin_score = db.Column(db.Integer)

    def update_scores(self,id):
        self.checkin_score=db.session.query(func.sum(Checkins.multiplier)).filter(Checkins.user_id ==id)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
 
    def get_json():
        users = User.query.order_by(User.checkin_score.desc()).all()
        data=[]
        for user in users:
            item = {"Username": user.username, "Score":user.checkin_score}
            data.append(item)
        return(data)
class Locations(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(64))
    events = db.relationship('Events', back_populates="location")

    def __str__(self):
        return self.location_name
  
class Checkins(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(64))
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    user=db.relationship('User', foreign_keys=[user_id] )
    multiplier= db.Column(db.Integer)

    def get_timeslot():
        current_hour = datetime.datetime.now().hour
        timeslot=0
        if current_hour >=6 and current_hour<=9:
            timeslot=1
        if current_hour >=10 and current_hour<=13:
            timeslot=2
        if current_hour >=14 and current_hour<=17:
            timeslot=3
        if current_hour >=18 and current_hour<=21:
            timeslot=4
        if current_hour >=22 and current_hour<=1:
            timeslot=5
        if (current_hour >=2 and current_hour<=5):
            timeslot=0
        return timeslot
    
    def get_todays_events(self):
        events = Events.query.order_by(Events.date).all()
        current_date=datetime.datetime.now(pytz.timezone('Canada/Pacific')).date()
        multiplier=1
        for event in events:
            if str(event.date.date()) == str(current_date):
                timeslot=Checkins.get_timeslot()
                if event.timeslot == timeslot:
                    print(self.location_name)
                    print(event.location)
                    if str(self.location_name) == str(event.location):
                        multiplier=event.multiplier
        
        return multiplier     
        

class Events(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    date= db.Column(db.DateTime)
    timeslot= db.Column(db.Integer)
    multiplier= db.Column(db.String(64))
    location_id=db.Column(db.ForeignKey("locations.id"), nullable=False)
    location = db.relationship('Locations', back_populates="events")


    def get_tableheaders1():
        events = Events.query.order_by(Events.date).all()
        dateslist=[]
        for event in events:
            dateslist.append(event.date.date())
        dateslist=set(dateslist)
        dateslist=sorted(dateslist)

        headers=[]
        for date in dateslist[1:]:
            headers.append(calendar.day_name[date.weekday()])
    
        return headers

    def get_tableheaders():
        events = Events.query.order_by(Events.date).all()
    
        headers=[]

        headers.append({
            "Timeslot":"6am -10am",
            "1":str(events[5].location) + "   "+ str(events[5].multiplier),
            "2":str(events[10].location) + "   "+ str(events[10].multiplier),
            "3":str(events[15].location) + "   "+ str(events[15].multiplier),
            "4":str(events[20].location) + "   "+ str(events[20].multiplier),
            "5":str(events[25].location) + "   "+ str(events[25].multiplier),
            "6":str(events[30].location) + "   "+ str(events[30].multiplier),
            "7":str(events[35].location) + "   "+ str(events[35].multiplier)
            })
        headers.append({
            
            "Timeslot":"10am -2pm",
            "1":str(events[6].location) + "   "+ str(events[6].multiplier),
            "2":str(events[11].location) + "   "+ str(events[11].multiplier),
            "3":str(events[16].location) + "   "+ str(events[16].multiplier),
            "4":str(events[21].location) + "   "+ str(events[21].multiplier),
            "5":str(events[26].location) + "   "+ str(events[26].multiplier),
            "6":str(events[31].location) + "   "+ str(events[31].multiplier),
            "7":str(events[36].location) + "   "+ str(events[36].multiplier)
            })
        headers.append({
            
            "Timeslot":"2pm -6pm",
            "1":str(events[7].location) + "   "+ str(events[7].multiplier),
            "2":str(events[12].location) + "   "+ str(events[12].multiplier),
            "3":str(events[17].location) + "   "+ str(events[17].multiplier),
            "4":str(events[22].location) + "   "+ str(events[22].multiplier),
            "5":str(events[27].location) + "   "+ str(events[27].multiplier),
            "6":str(events[32].location) + "   "+ str(events[32].multiplier),
            "7":str(events[37].location) + "   "+ str(events[37].multiplier),
            })
        headers.append({
            
            "Timeslot":"6pm -10pm",
            "1":str(events[8].location) + "   "+ str(events[8].multiplier),
            "2":str(events[13].location) + "   "+ str(events[13].multiplier),
            "3":str(events[18].location) + "   "+ str(events[18].multiplier),
            "4":str(events[23].location) + "   "+ str(events[23].multiplier),
            "5":str(events[28].location) + "   "+ str(events[28].multiplier),
            "6":str(events[33].location) + "   "+ str(events[33].multiplier),
            "7":str(events[38].location) + "   "+ str(events[38].multiplier)
            })
        headers.append({
            
            "Timeslot":"10pm -2am",
            "1":str(events[9].location) + "   "+ str(events[9].multiplier),
            "2":str(events[14].location) + "   "+ str(events[14].multiplier),
            "3":str(events[19].location) + "   "+ str(events[19].multiplier),
            "4":str(events[24].location) + "   "+ str(events[24].multiplier),
            "5":str(events[29].location) + "   "+ str(events[29].multiplier),
            "6":str(events[34].location) + "   "+ str(events[34].multiplier),
            "7":str(events[39].location) + "   "+ str(events[39].multiplier)
            })
        
        return headers

        
    

class EventsView(ModelView):
    can_delete=False
    form_columns=["date","timeslot","multiplier","location"]
    column_list=["date","timeslot","multiplier","location"]

admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Locations,db.session))
admin.add_view(ModelView(Checkins,db.session))
#admin.add_view(ModelView(Events,db.session))
admin.add_view(EventsView(Events,db.session))
#class Recipe(db.Model):
#    id=db.Column(db.Integer, primary_key = True)
#    title = db.Column(db.String(100), nullable = False)
#    description = db.Column(db.Text, nullable = False)
#    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


#class SharedRecipe(db.Model):
##    id=db.Column(db.Integer, primary_key=True)
#    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable = False)
#    sharer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
#    sharee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#    recipe = db.relationship('Recipe',backref=db.backref('shared_recipes'), lazy=True)
#    sharer =db.relationship('User', foreign_keys = [sharer_id])
#    sharee= db.relationship('User', foreign_keys =[sharee_id])

