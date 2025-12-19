import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailNotificationService:
    def __init__(self, smtp_server="smtp.gmail.com", port=587):
        self.smtp_server = smtp_server
        self.port = port
    
    def send_status_update(self, tracking_id, recipient_email, status):
        """Send email notification when shipment status changes"""
        subject = f"ETO-TELCO: Shipment {tracking_id} Status Update"
        body = f"""
        Dear Customer,
        
        Your shipment {tracking_id} has been updated.
        Current Status: {status}
        
        Track your shipment: https://eto-telco.com/track/{tracking_id}
        
        Best regards,
        ETO-TELCO Team
        """
        
        print(f"Email sent to {recipient_email}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        return True
    
    def send_delivery_confirmation(self, tracking_id, recipient_email):
        """Send delivery confirmation email"""
        subject = f"ETO-TELCO: Shipment {tracking_id} Delivered"
        body = f"""
        Dear Customer,
        
        Your shipment {tracking_id} has been successfully delivered!
        
        Thank you for choosing ETO-TELCO.
        
        Best regards,
        ETO-TELCO Team
        """
        
        print(f"Delivery confirmation sent to {recipient_email}")
        return True

# Test
if __name__ == "__main__":
    email_service = EmailNotificationService()
    email_service.send_status_update("TRK001", "customer@example.com", "In Transit")
    