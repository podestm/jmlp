from flask import Flask
from auth_views import auth_bp              # This should be from auth_views, not auth
from admin_views import admin_bp
from public_views import public_bp
from models import User
from config import db                       # Import db from extensions
from flask_login import LoginManager
from flask_migrate import Migrate
from pytz import timezone


app = Flask(__name__)
app.config["DEBUG"] = True


SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="michalpodest",
    password="jmlptest",
    hostname="michalpodest.mysql.pythonanywhere-services.com",
    databasename="michalpodest$comments",
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'jmlpwebsecretkey'



# Initialize the configs
db.init_app(app)  # Initialize the db instance with the app
migrate = Migrate(app, db)




# Initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Set the default login view



# Define the timezone for Prague
prague_tz = timezone('Europe/Prague')



#Login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()




# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(public_bp)
