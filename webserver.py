 # -*- coding: utf-8 -*-
from    flask import Flask,render_template,redirect,abort,request,session,url_for,flash
from    flask_bootstrap import Bootstrap
from    flask_moment import Moment
from    flask_wtf import FlaskForm
from    flask_pymongo import PyMongo
from    flask_login import LoginManager,UserMixin,login_required,login_user,logout_user
from    flask_babel import Babel,lazy_gettext,gettext
from    wtforms import *
from    wtforms.validators import *
from    flask_mail import Mail,Message
from    threading import  Thread
import  paramiko,base64,datetime,os,threading,logging

log = logging.getLogger()
log.setLevel(level = logging.DEBUG)
logfile = logging.FileHandler('log/log.txt',encoding='utf-8')
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
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
# 设置当未登录用户请求一个只有登录用户才能访问的视图时，闪现的错误消息的内容，
# 默认的错误消息是：Please log in to access this page.。
login_manager.login_message = '请先登录'
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


@login_manager.user_loader
def load_user(username):
    if mongo.db.user.find_one({"name": username}) is not None:
        curr_user = User()
        curr_user.id = username
        return curr_user



@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html',current_time=datetime.datetime.utcnow())


@app.route('/loginsuc',methods=['GET'])
@login_required
def login_suc():
    return render_template('login_suc.html')

@app.route('/',methods=['GET','POST'])
def login():
    form = NameForm()
    user = None
    pwd = None
    if  form.validate_on_submit():
        session['user'] = form.user.data
        session['pwd'] = form.password.data
        form.user.data = ''
        form.password.data = ''
        userinfo = mongo.db.user.find_one({"name":session['user']})
        if userinfo is  not None and userinfo['pwd'] == session['pwd']:
            flash('Login successfully!')
            log.info('%s 登录成功' % session['user'])
            curr_user = User()
            curr_user.id = session['user']
            login_user(curr_user,remember=True)
            next = request.args.get('next')
            log.info(next)
            return redirect(url_for('login_suc'))
        else:
            log.info('%s 登录失败' % session['user'])
            flash('账号不存在或密码错误')

    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

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


######测试上传
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save('E:/tmp/%s' % f.filename)
        flash('You were successfully logged in')
        return '上传成功'
    return render_template('upload.html')



@app.route('/chpwd',methods=['GET'])
def chpwd_page():
    return render_template('learn.html')



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')



if __name__=='__main__':
    app.run('0.0.0.0',8080,debug=True)

