# -*- coding: utf-8 -*-
from    flask_mail import Mail,Message
msg = Message('test subject', sender='you@example.com',recipients=['545943059@qq.com'])
msg.body = 'text body'
msg.html = '<b>HTML</b> body'
with app.app_context():
    mail.send(msg)