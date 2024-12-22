import json

class create_alerts:
    def __init__(self) -> None:
        self.contact_info = json.load('info.json')
        pass

    def get_info(self):
        send_emails = self.contact_info["EmailAlerts"]
        send_texts = self.contact_info["TextAlerts"]
        if send_emails == 1:
            self.email = self.contact_info["Email"]
            self.send_emails = True
        else:
            self.email = None
            self.send_emails = False
        
        if send_texts == 1:
            self.phone_number = self.contact_info["PhoneNumber"]
            self.send_texts = True
        else:
            self.phone_number = None
            self.send_texts = False
        return send_texts, send_emails, self.email, self.phone_number
    
    def email_alerts(self):
        pass
    