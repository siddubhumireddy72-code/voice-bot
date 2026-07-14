"""Call Management System"""
import logging
from datetime import datetime
from database.models import db, Call
from call_handler.asterisk_handler import AsteriskHandler

logger = logging.getLogger(__name__)


class CallManager:
    """Manages call lifecycle"""
    
    def __init__(self):
        self.asterisk_handler = AsteriskHandler()
        self.calls = {}  # Active calls
    
    def handle_incoming_call(self, call_data):
        """Handle incoming call event"""
        try:
            caller_number = call_data.get('from')
            receiver_number = call_data.get('to')
            channel = call_data.get('channel')
            
            # Create call record
            call = Call(
                caller_number=caller_number,
                receiver_number=receiver_number,
                call_type='inbound',
                status='answered'
            )
            db.session.add(call)
            db.session.commit()
            
            logger.info(f"Incoming call from {caller_number} to {receiver_number}")
            
            # Store in active calls
            self.calls[channel] = {
                'call_id': call.id,
                'channel': channel,
                'caller': caller_number,
                'receiver': receiver_number,
                'started_at': datetime.utcnow()
            }
            
            return {
                'call_id': call.id,
                'status': 'received',
                'caller': caller_number
            }
        except Exception as e:
            logger.error(f"Error handling incoming call: {str(e)}")
            raise
    
    def end_call(self, channel):
        """End a call"""
        try:
            if channel in self.calls:
                call_info = self.calls[channel]
                call_id = call_info['call_id']
                
                # Update call record
                call = Call.query.get(call_id)
                if call:
                    call.status = 'ended'
                    call.ended_at = datetime.utcnow()
                    call.duration = int((call.ended_at - call.started_at).total_seconds())
                    db.session.commit()
                
                logger.info(f"Call ended: {call_id}")
                del self.calls[channel]
                return True
        except Exception as e:
            logger.error(f"Error ending call: {str(e)}")
        return False
    
    def get_active_calls(self):
        """Get all active calls"""
        return self.calls
    
    def get_call_info(self, channel):
        """Get info about specific call"""
        return self.calls.get(channel)
