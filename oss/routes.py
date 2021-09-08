
from flask import render_template, url_for, redirect, request
from flask.helpers import flash
from flask_login import login_user, current_user, logout_user, login_required
from oss.forms import RegisterForm, LoginForm, AddAdmin, CreateOSS, OSSSubmission
from oss.models import Submission, User, Oss
from oss import app, db, bcrypt
from datetime import timedelta


@app.route("/")
@app.route("/oss")
def home():
    global current_oss
    if Oss.query.first():
        oss_list = Oss.query.all()
        current_oss = oss_list[-1]
    prev_oss = Oss.query.all()
    del prev_oss[-1] # removing current OSS from list of previous OSS
    prev_oss.reverse() # reversing previous OSS list to get it in chronological order
    admin_posted = User.query.filter_by(id=current_oss.admin_posted).first().name

    #gettting date added
    beg_date = current_oss.date_posted + timedelta(days=1) #submission date for beginner
    ad_date = current_oss.date_posted + timedelta(days=3) #submission date for advance
    return render_template("home.html", current_oss=current_oss, admin_posted=admin_posted, prev_oss=prev_oss, beg_date=beg_date, ad_date=ad_date)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Your account is successfully created. You can take part in OSS now!', 'success')
        return redirect(url_for("home"))
    return render_template("register.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login unsuccessful. Try Again.", "danger")
    return render_template("login.html", form=form)

# OSS is created here by admins
@app.route("/createoss", methods=['GET', 'POST'])
@login_required
def create_oss():
    if current_user.user != "admin":
        return redirect(url_for("home"))
    form = CreateOSS()
    if form.validate_on_submit():
        oss = Oss(title=form.title.data, premise=form.premise.data, challenge=form.challenge.data, beginner=form.beginner.data, intermediate=form.intermediate.data, advance=form.advance.data, admin_posted = current_user.id)
        db.session.add(oss)
        db.session.commit()
        flash("New OSS successfully posted", "success")
        return redirect(url_for("home"))
    else:
        flash("Unsuccessful. Try again.", "danger")
    return render_template("create.html", form=form)

# OSS project is submitted here
@app.route("/submit", methods=['GET', 'POST'])
@login_required
def submit_oss():
    form = OSSSubmission()
    if form.validate_on_submit():
        submission = Submission(github=form.github.data, description=form.description.data, user_submitted=current_user.name, oss_id=current_oss.id, level=form.level.data)
        db.session.add(submission)
        db.session.commit()
        flash("Successfully Submitted", "success")
        return redirect(url_for("home"))
    return render_template("submit.html", form=form)

# all submissions of the current OSS can be viewed
@app.route("/submissions/<int:oss_id>")
def view_submissions(oss_id):
    submissions = Submission.query.filter_by(oss_id=oss_id).all()
    return render_template("submissions.html", submissions=submissions)

# admins can be added by other admins
@app.route("/addadmin", methods=['GET', 'POST'])
@login_required
def add_admin():
    if current_user.user != "admin":
        return redirect(url_for("home"))
    form = AddAdmin()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data):
            user = User.query.filter_by(email=form.email.data).first()
            user.user = "admin"
            db.session.add(user)
            db.session.commit()
            flash(f"{user.name} is an admin.", "success")
            return redirect(url_for('home'))
    else:
        flash("Email not valid", "danger")
    return render_template("add_admin.html", form=form)

# personal details and previous OSS participated in are shown
@app.route("/account")
@login_required
def account():
    for submission in current_user.submissions:
        oss_all = Oss.query.filter_by(id=submission.oss_id).all()
    return render_template("account.html", oss_all=oss_all)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))