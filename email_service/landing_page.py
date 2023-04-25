def landing_email_send(emailEnd:str):

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    import requests
    from io import BytesIO
    from PIL import Image
    import os


    response = requests.get('https://i.ibb.co/h28SwBQ/swaron-2.jpg')
    img = Image.open(BytesIO(response.content))

    mailserver = smtplib.SMTP(os.getenv('EMAIL_SERVER'), 587)
    mailserver.starttls()
    mailserver.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))

    email_msg = MIMEMultipart('related')
    email_msg['From'] = os.getenv('EMAIL_USER')
    email_msg['To'] = emailEnd
    email_msg['Subject'] = 'Welcome to Swaron!'

    msgAlternative = MIMEMultipart('alternative')
    email_msg.attach(msgAlternative)

    msgText = MIMEText(f"""

    <center><br><img src="cid:image1" width="350" height="auto"><br></center>

    """,

                       'html')

    msgAlternative.attach(msgText)

    img_io = BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)
    msgImage = MIMEImage(img_io.read())

    msgImage.add_header("Content-ID", '<image1>')
    email_msg.attach(msgImage)

    mailserver.sendmail(os.getenv("EMAIL_USER"), emailEnd, email_msg.as_string())
    mailserver.quit()
