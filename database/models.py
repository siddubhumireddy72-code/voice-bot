"""Database Models for Voice Bot"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Call(db.Model):
    """Call record model"""
    __tablename__ = 'calls'
    
    id = db.Column(db.Integer, primary_key=True)
    caller_number = db.Column(db.String(20), nullable=False)
    receiver_number = db.Column(db.String(20), nullable=True)
    duration = db.Column(db.Integer, default=0)  # Duration in seconds
    status = db.Column(db.String(20), default='pending')  # pending, answered, missed, ended
    transcript = db.Column(db.Text, nullable=True)
    bot_response = db.Column(db.Text, nullable=True)
    call_type = db.Column(db.String(20), default='inbound')  # inbound, outbound
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'caller_number': self.caller_number,
            'receiver_number': self.receiver_number,
            'duration': self.duration,
            'status': self.status,
            'transcript': self.transcript,
            'bot_response': self.bot_response,
            'call_type': self.call_type,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Transcript(db.Model):
    """Call transcript model"""
    __tablename__ = 'transcripts'
    
    id = db.Column(db.Integer, primary_key=True)
    call_id = db.Column(db.Integer, db.ForeignKey('calls.id'), nullable=False)
    speaker = db.Column(db.String(20), default='user')  # user, bot
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    call = db.relationship('Call', backref=db.backref('transcripts', lazy=True))
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'call_id': self.call_id,
            'speaker': self.speaker,
            'text': self.text,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }


class BotResponse(db.Model):
    """Bot response log model"""
    __tablename__ = 'bot_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    call_id = db.Column(db.Integer, db.ForeignKey('calls.id'), nullable=False)
    user_input = db.Column(db.Text, nullable=False)
    bot_output = db.Column(db.Text, nullable=False)
    model_used = db.Column(db.String(50), default='gpt-3.5-turbo')
    tokens_used = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    call = db.relationship('Call', backref=db.backref('bot_responses', lazy=True))
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'call_id': self.call_id,
            'user_input': self.user_input,
            'bot_output': self.bot_output,
            'model_used': self.model_used,
            'tokens_used': self.tokens_used,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
