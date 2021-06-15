from flask import Flask
from flask_mail import Mail, Message
import random

app = Flask(__name__)
mail= Mail(app)
#CONFIGURATIONS FOR GMAIL
sender = 'saurabh9759mishra@gmail.com'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = sender
app.config['MAIL_PASSWORD'] = 'callmesaurabh'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/failure_mail/<exception>")
def send_mail(exception):
   receiver = "saurabh975mishra@gmail.com"
   msg = Message('noReply', sender = sender, recipients = [receiver])
   msg.body = exception
   mail.send(msg)
   return msg.body

if __name__ == '__main__':
   app.run(debug = True,port=8989)

