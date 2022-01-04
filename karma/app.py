from flask import request, render_template, redirect, abort, url_for
from flask_login import LoginManager, login_required, login_user
from flask_login import logout_user, current_user
from karma.flask_app import FlaskApp
from karma.database import db
from karma.model.job import Job, JobType, JobConverter
from karma.model.user import User
from karma.model.award import Award


app = FlaskApp(__name__)
app.secret_key = '5WCMvGdgSGIHL6nF3QJQ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///karma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.url_map.converters['jobtype'] = JobConverter
db.init_app(app)

# implement LoginManager
auth = LoginManager()
auth.init_app(app)


@auth.user_loader
def load_user(user_id):
    with db:
        user = db.get(User).where(User.name, user_id).first()
        return user


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form['username']
        password = request.form['password']

        with db:
            user = db.get(User).where(User.name, username).first()
            if user is None:
                abort(404)

            is_valid = user.validate_password(password)
            if is_valid:
                user.authenticated = True
                login_user(user, remember=True)
                return redirect(url_for("entry"))
            else:
                abort(401)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    with db:
        db.add(user)
    logout_user()
    return redirect(url_for("login"))


@auth.unauthorized_handler
def unauthorized_callback():
    return redirect(f'/login?next={request.path}')


@app.route('/', methods=['GET'])
@login_required
def entry():
    user = current_user
    return redirect(f'/users/{user.name}')


def user_authorization(func):
    def wrapper(*args, **kwargs):
        user = current_user
        if 'username' not in kwargs:
            return abort(400)
        username = kwargs['username']
        if username != user.name and not user.is_admin:
            return abort(401)
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


def admin_authorization(func):
    def wrapper(*args, **kwargs):
        user = current_user
        if not user.is_admin:
            return abort(401)
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@app.route('/users', methods=['GET'])
@login_required
@admin_authorization
def users():
    with db:
        users = db.get(User).all()
        return render_template("users.html", users=users)


@app.route('/users/<username>', methods=['GET'])
@login_required
@user_authorization
def user(username):
    with db:
        user = db.get(User).where(User.name, username).first()
        return render_template("user.html", user=user, viewer=current_user)


@app.route('/users/<username>/awards', methods=['GET', 'POST'])
@login_required
@user_authorization
def awards(username):
    if request.method == 'GET':
        with db:
            user = db.get(User).where(User.name, username).first()
            return render_template('awards.html', user=user)
    elif request.method == 'POST':
        with db:
            user = db.get(User).where(User.name, username).first()
            user.add(Award())
        return redirect(url_for("user", username=username))


@app.route('/users/<username>/awards/register', methods=['GET', 'POST'])
@login_required
@admin_authorization
def register_award_for_user(username):
    with db:
        user = db.get(User).where(User.name, username).first()
        return render_template('award-add.html', user=user)


@app.route('/users/<username>/jobs', methods=['GET', 'POST'])
@login_required
@user_authorization
def jobs(username):
    if request.method == 'GET':
        with db:
            user = db.get(User).where(User.name, username).first()
            return render_template('jobs.html', user=user)
    elif request.method == 'POST':
        job_done = request.form['jobType']
        with db:
            user = db.get(User).where(User.name, username).first()
            user.add(Job(JobType.parse(job_done)))
            return redirect(url_for("job_added", username=username))


@app.route('/users/<username>/jobs/added', methods=['GET'])
@login_required
@user_authorization
def job_added(username):
    with db:
        user = db.get(User).where(User.name, username).first()
        return render_template('job-done.html', user=user)


@app.route('/users/<username>/jobs/<jobtype:job>', methods=['GET'])
@login_required
@user_authorization
def add_job_for_user(username, job):
    with db:
        user = db.get(User).where(User.name, username).first()
        return render_template('job-add.html', user=user, jobtype=job)


@app.route('/users/<username>/jobs/register', methods=['GET'])
@login_required
@user_authorization
def register_job_for_user(username):
    with db:
        user = db.get(User).where(User.name, username).first()
        jobtypes = [choice for choice in JobType]
        return render_template('job-select-add.html',
                               user=user, jobtypes=jobtypes)


@app.route('/jobs/<jobtype:job>/add', methods=['GET'])
@login_required
def add_job(job):
    """ General entry to add a job for all users. Can be used for QR code
        scanning and redirects to user specific job registration. """
    username = current_user.name
    return redirect(url_for('add_job_for_user', username=username,
                    job=job))


@app.errorhandler(404)
def not_found(e):
    return render_template("error-code.html",
                           response_status='404 not found'), 404


@app.errorhandler(400)
def bad_request(e):
    return render_template("error-code.html",
                           response_status='400 bad request'), 400


@app.errorhandler(401)
def not_authorized(e):
    return render_template("error-code.html",
                           response_status='401 not authorized'), 401


@app.errorhandler(500)
def server_error(e):
    return render_template("error-code.html",
                           response_status='500 server error'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)
