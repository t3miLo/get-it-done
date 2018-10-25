from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from form import RegisterForm, LoginForm

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Jeremiah1010'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:Jeremiah1010@localhost:3306/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, owner):
        self.name = name
        self.completed = False
        self.owner = owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    task = db.relationship('Task', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/', methods=['POST', 'GET'])
def index():
    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name, owner)
        db.session.add(new_task)
        db.session.commit()
    users = User.query.all()
    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()

    return render_template('todos.html', title="Get It Done!", tasks=tasks, completed_tasks=completed_tasks, users=users)


@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()
        flash('You account has been created! You are now able to login.')
        return redirect('/')
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username = form.username.data
    password = form.password.data
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        print('User = ', user, 'password = ', user.password)
        if user and user.password == password:
            session['username'] = username
            flash('You where able to login!', 'success')
            return redirect('/')
        else:
            print('wrong')
            flash('Login Unsuccessful, Please Check Username and Password', 'error')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    del session['username']


@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('login')


if __name__ == '__main__':
    app.run()


# working on who is the owner;
