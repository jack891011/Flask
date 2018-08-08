 # -*- coding: utf-8 -*-
from    flask import Flask,render_template,redirect,abort,request,session,url_for,flash
from    flask_bootstrap import Bootstrap
from    flask_moment import Moment
from    flask_wtf import FlaskForm
from    flask_pymongo import PyMongo
from    flask_login import LoginManager,UserMixin,login_required,login_user
from    flask_babel import Babel,lazy_gettext,gettext
from    wtforms import *
from    wtforms.validators import *
from    flask_mail import Mail,Message
from    threading import  Thread
import  paramiko,base64,datetime,os,threading,logging

log = logging.getLogger()
log.setLevel(level = logging.DEBUG)
logfile = logging.FileHandler('log.txt')
logfile.setLevel(logging.INFO)
screen = logging.StreamHandler()
screen.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logfile.setFormatter(formatter)
log.addHandler(logfile)
log.addHandler(screen)



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
app.config['MONGO_URI'] = 'mongodb://192.168.1.49:40000/flask'

bootstrap = Bootstrap(app)
moment = Moment(app)
mail = Mail(app)
mongo = PyMongo(app)
babel = Babel(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# 设置当未登录用户请求一个只有登录用户才能访问的视图时，闪现的错误消息的内容，
# 默认的错误消息是：Please log in to access this page.。
login_manager.login_message = 'Unauthorized User'
# 设置闪现的错误消息的类别
login_manager.login_message_category = "info"


@babel.localeselector
def get_locale():
     return 'zh'

@babel.timezoneselector
def get_timezone():
     return 'UTC+8'


class NameForm(FlaskForm):
    user = StringField('Uasename',validators=[Email()], render_kw = {'placeholder':'输入你的用户名'})
    password = PasswordField('Password',validators=[DataRequired()],render_kw = {'placeholder':'输入你的密码'})
    submit = SubmitField('Login in')
    #email = StringField('Email Address', validators=[Email()])
    #password2 = PasswordField('', [DataRequired(),EqualTo('password', message='Passwords must match')],
                              #render_kw = {'placeholder':'再次输入你的密码'}) #Text Field类型，密码输入框，必填，必须同password字段一致,适用于密码二次确认
    #age = IntegerField('Age', validators=[NumberRange(min=16, max=70)]) # Text Field类型，文本输入框，必须输入整型数值，范围在16到70之间
    #birthday = DateField('Birthday', format='%Y-%m-%d')  # Text Field类型，文本输入框，必须输入是"年-月-日"格式的日期
    #choice = SelectMultipleField('Hobby', choices=[('swim', 'Swimming'),('skate', 'Skating'),('hike', 'Hiking')]) #Select类型，多选框，choices里的内容会在Option里，里面每个项是(值，显示名)对
    #job = SelectField('', render_kw = {'placeholder':'输入你的职业'},choices=[('teacher', 'Teacher'),('doctor', 'Doctor'),('engineer', 'Engineer'),('lawyer', 'Lawyer')]) #下拉选框

class User(UserMixin):
    pass


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html',current_time=datetime.datetime.utcnow())


@app.route('/loginsuc',methods=['GET'])
def login_suc():
    return render_template('login_suc.html')

@app.route('/login',methods=['GET','POST'])
def login_page():
    form = NameForm()
    user = None
    pwd = None
    if  form.validate_on_submit():
        session['user'] = form.user.data
        session['pwd'] = form.password.data
        form.user.data = ''
        form.password.data = ''
        if mongo.db.user.find_one({"name":session['user']}) is not None:
            flash('Login successfully!')
            log.info('%s 登录成功' % session['user'])
            return redirect(url_for('login_suc'))
        else:
            log.info('%s 登录失败' % session['user'])
            flash('账号不存在,请注册')
            #thr = Thread(target=send_email,args=(session['user'],))
            #thr.start()
            #return redirect(url_for('login_bad'))
    return render_template('login.html',form=form)

############################# 测试 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def send_email(to):
    app.app_context().push()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'],sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = '感谢注册'
    mail.send(msg)

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



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')



if __name__=='__main__':
    app.run('0.0.0.0',8080,debug=True)

