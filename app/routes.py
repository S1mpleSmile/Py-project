from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user
from app import app, db
from app.forms import loginform
from app.models import Users, Profiles, NewPost
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
# @login_required
def index():
    info = []
    info = NewPost.query.all()
    list = []
    list = info[0:min(15, len(info))]

    return render_template('index.html', title="Home", list=list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = loginform()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/add_post', methods=["POST", "GET"])
def addPost():
    print("2")
    # if request.method == "POST":
    p = NewPost(name=request.form['name'], title=request.form['post'])
    # if request.method >= 4 and request.form['post'] >= 18:
    db.session.add(p)
    db.session.commit()
    # else:


@app.route('/register', methods=("POST", "GET"))
def register():
    if request.method == "POST":
        # здесь должна быть проверка корректности введенных данных
        try:
            hash = generate_password_hash(request.form['psw'])
            u = Users(email=request.form['email'], psw=hash)
            db.session.add(u)
            db.session.flush()

            p = Profiles(name=request.form['name'], old=request.form['old'],
                         city=request.form['city'], user_id=u.id)
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")

        return redirect(url_for('index'))

    return render_template("register.html", title="Registration")


@app.route('/profile')
@login_required
def profile():
    user = Profiles.query.filter_by(id=current_user.id).first()
    return render_template('profile.html', user=user)


current_page = []


@app.route("/page/<int:id_post>", methods=["POST", "GET"])
def page(id_post):
    if request.method == "POST":
        smth = NewPost.query.filter(NewPost.id_post == id_post).first_or_404()
        db.session.delete(smth)
        title = request.form.get('name')
        post = request.form.get('post')
        photo = request.form.get('photo')
        p = NewPost(title, post, photo)
        db.session.add(p)
        db.session.commit()
        return render_template("page.html", page=p)
    else:
        p = NewPost.query.filter(NewPost.id_post == id_post).first_or_404()
        return render_template('page.html', page=p)


@app.route("/searched", methods=["POST", "GET"])
def searched():
    title = request.form.get('s')
    try:
        p = NewPost.query.filter(NewPost.name == title).first_or_404()
    except:
        return redirect(url_for('index'))
    return render_template('searched.html', page=p)



@app.route('/add_page', methods=["POST", "GET"])
def add_page():
    if request.method == "POST":
        # name = current_user.__name
        title = request.form.get('name')
        post = request.form.get('post')
        photo = request.form.get('photo')
        p = NewPost(title, post, photo)
        db.session.add(p)
        db.session.commit()
        return render_template("page.html", page=p)
    else:
        return render_template("add_post.html")


@app.route('/search')
def search():
    return render_template("page.html", page=current_page)


@app.route('/edit/<int:id_post>')
def edit(id_post):
    p = NewPost.query.filter(NewPost.id_post == id_post).first_or_404()
    return render_template('edit.html', page=p)