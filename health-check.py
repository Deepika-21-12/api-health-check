import smtplib
import os
import urllib.request
from datetime import datetime
from email.mime.text import MIMEText

sender_email = os.environ.get("EMAIL_ADDRESS")     #"deepikapalanisamy2001@gmail.com"
receiver_email = "deepikaadeepi01@gmail.com"     # Can be the same or different
app_password = os.environ.get("EMAIL_PASSWORD")    #"tjhv ciwn qjjr zswk"  
url = "https://invivodb.rd.astrazeneca.net:7011/invivodb/study/josso_login.jsp"


def check_api_health(url):
    try:
        with urllib.request.urlopen(url) as response:
            status = response.status
            print(f"status: {status}")
            return status==200, status
    except urllib.error.HTTPError as e:
        return False, e.code
    except Exception as e:
        return False, str(e)
    
    
def create_mail_body(url, error_message):
    subject = "API Downtime Reported"
    time_of_outage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body = f''' The API at {url} is currently DOWN - {time_of_outage}. Error:{error_message} 
    '''
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    
    return msg.as_string()
    
    
def send_mail(url, error_message):
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            msg = create_mail_body(url, error_message)
            print(f"Message : {msg}")
            server.sendmail(sender_email, receiver_email, msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


is_healthy, error_message = check_api_health(url)
if not is_healthy:
    print("sending mail...")
    send_mail(url,error_message)
