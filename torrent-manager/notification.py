import requests
import logging
from typing import Dict, Any

class NotifiarrNotifier:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Notifiarr notification client
        
        :param config: Configuration dictionary containing Notifiarr settings
        """
        self.api_key = config.get('notifications', {}).get('notifiarr_api_key')
        self.api_url = 'https://notifiarr.com/api/v1/notification'
        self.logger = logging.getLogger(__name__)
        
        if not self.api_key:
            self.logger.warning("Notifiarr API key not configured")
    
    def send_notification(self, message: str, level: str = 'info'):
        """
        Send notification to Notifiarr
        
        :param message: Notification message text
        :param level: Notification level (info, warning, error)
        """
        if not self.api_key:
            self.logger.warning("Cannot send notification - API key missing")
            return
        
        try:
            payload = {
                'notification': {
                    'message': message,
                    'level': level
                }
            }
            
            headers = {
                'Content-Type': 'application/json',
                'apikey': self.api_key
            }
            
            response = requests.post(
                self.api_url, 
                json=payload, 
                headers=headers
            )
            
            # Check if notification was successful
            if response.status_code != 200:
                self.logger.error(f"Failed to send Notifiarr notification: {response.text}")
        
        except Exception as e:
            self.logger.error(f"Error sending Notifiarr notification: {e}")

def send_notification(message: str, config: Dict[str, Any], level: str = 'info'):
    """
    Wrapper function to send notifications
    
    :param message: Notification message
    :param config: Configuration dictionary
    :param level: Notification level
    """
    try:
        notifier = NotifiarrNotifier(config)
        notifier.send_notification(message, level)
    except Exception as e:
        logging.error(f"Notification failed: {e}")