import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def send_mail(text, subject, fromEmail, recipients, username, password):
    assert isinstance(recipients, list)

    msg = MIMEMultipart("alternative")
    msg["from"] = fromEmail
    msg["to"] = ", ".join(recipients)
    msg["subject"] = subject


    txtPart = MIMEText(text, "plain")
    msg.attach(txtPart)

    # htmlPart = MIMEText("<h1> This is working </h1>"
    # msg.attach(htmlPart)
    msgStr = msg.as_string()
    # login
    server = smtplib.SMTP(host="smtp.gmail.com", port=587)   
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.sendmail(username, recipients, msgStr)
    server.quit()

