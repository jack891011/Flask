 # -*- coding: utf-8 -*-
from flask import Flask,render_template,redirect,abort,request,session,url_for,flash
from  flask_bootstrap import Bootstrap
from  flask_moment import Moment
from flask_wtf import FlaskForm
from  flask_pymongo import PyMongo
from wtforms import *
from wtforms.validators import *
from    flask_mail import Mail,Message
import paramiko,base64,datetime,os,threading
from threading import  Thread


app = Flask(__name__)
##############################  app 配送段 ################
app.app_context().push()
app.config['SECRET_KEY']='beckham07'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flask]'
app.config['FLASKY_MAIL_SENDER'] = 'Flask Admin <13851543835@163.com>'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USERNAME'] = '13851543835@163.com'
app.config['MAIL_PASSWORD'] = 'beckham07'
app.config['MONGO_URI'] = 'mongodb://192.168.1.49:40000/admin'

bootstrap = Bootstrap(app)
moment = Moment(app)
mail = Mail(app)
mongo = PyMongo(app)


class NameForm(FlaskForm):
    name = StringField('输入你的账号',validators=[Email()])
    submit = SubmitField('提交')

#form = NameForm()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html',current_time=datetime.datetime.utcnow())


@app.route('/login',methods=['GET'])
def login_page():
    return render_template('login.html')



@app.route('/base', methods=['GET', 'POST'])
def base():
    return render_template('base1.html')

@app.route('/base1', methods=['GET', 'POST'])
def foir():
    return redirect(url_for('home'))

@app.route('/login',methods=['POST'])
def login():
    user=request.form['username']
    passwd=request.form['password']


    if db.find_one({'user':user})['pwd'] == passwd:
            return render_template('login_suc.html')
    else:
              return render_template('login_bad.html')

@app.route('/flask/<user>')
def flask(user):
    form = NameForm()
    #user = { 'nickname': 'Miguel' } # fake user
    #return render_template("hello.html",
        #title = 'Home',
        #user = user)
    #return redirect('http://www.sina.com')

    return render_template('user.html',form=form,name=user)

############################# 测试 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def send_email(to):
    app.app_context().push()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'],sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = '感谢注册'
    mail.send(msg)

@app.route('/test', methods=['GET', 'POST'])
def test():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        if mongo.db.user.find_one({"name":session['name']}) is not None:
            return redirect(url_for('home'))
        else:
            flash('账号不存在,请注册')
            thr = Thread(target=send_email,args=(session['name'],))
            thr.start()
            return redirect(url_for('test'))
    return render_template('test.html',form=form, name=session.get('name'))


############################# 发送邮件 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/mail')
def send_mail():
    msg = Message('测试主题',
                  sender=('Flask Admin', '13851543835@163.com'),
                  recipients=['545943059@qq.com'])
    msg.html = '<h1>这是一封测试主题的邮件，请阅后即焚</h1>'
    mail.send(msg)
    return 'Successful'




@app.route('/chpwd',methods=['GET'])
def chpwd_page():
    return render_template('learn.html')


@app.route('/chpwd',methods=['POST'])
def chpwd():
    host='192.168.1.52'
    pwd= base64.decodebytes(b'YmVja2hhbTIz\n')
    user=request.form['a']
    #pwd=request.form['b']
    npwd=request.form['c']
    cmd="echo %s:%s | chpasswd " % (user,npwd)
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())   #自动添加主机名和主机密钥到本地的hostkeys对象
    ssh.connect(hostname=host,username='root',password=pwd)
    stdin,stdout,stderr=ssh.exec_command(cmd)
    print(stdout.read())
    return render_template('login_suc.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')



if __name__=='__main__':
    app.run('192.168.1.8',8080,debug=True)

