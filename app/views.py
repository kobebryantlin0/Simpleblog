from app import app, lm
from flask import render_template, flash, redirect, session, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LogonForm, RegisterForm, ChangePasswordForm
from .models import User
from . import db


@app.route('/')
@app.route('/index')
# @login_required
def index():
    return render_template('index.html',
                           title = '首页')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LogonForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('账号或密码无效。')
    return render_template('login.html',
                           title = '登录',
                           form =form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经登出账号。')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    nickname=form.nickname.data,
                    password=form.password.data)
        db.session.add(user)
        flash('你可以登录了。')
        return redirect(url_for('login'))
    return render_template('register.html',
                           form=form,
                           title='注册')

@app.route('/changepassword', methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('你的密码已经更改。')
            return redirect(url_for('index'))
        else:
            flash('无效的密码。')
    return render_template('change_password.html',
                           form=form,
                           title='更改密码')

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('未发现用户：' + nickname)
        return redirect(url_for('index'))
    return render_template('user.html',
                           user=user,
                           title='个人资料')
