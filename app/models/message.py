from db import db

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.Unicode())
    ##реализуем позже
    ##publication_time = db.Column(db.Date)
    # связи
    thread_id = db.Column(db.Integer(), db.ForeignKey('threads.id'))





    