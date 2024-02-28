import os.path
import pathlib
import cachecontrol
import google
import requests
from flask_login import login_required, logout_user, login_user, current_user
from flask import Blueprint, redirect, render_template, request, flash, session as sess, url_for
from flask_dance.contrib.github import make_github_blueprint, github
from google.oauth2 import id_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from zenora import APIClient

from google_auth_oauthlib.flow import Flow
from logic.facade import LogicFacade
from presentation.UserLogin import UserLogin

engine = create_engine(
    'postgresql://postgres:postgres@localhost/postgres',
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()
online_users = []

logic = LogicFacade(session)

auth_bp = Blueprint('auth', __name__)

GOOGLE_CLIENT_ID = "823988869838-v3amhjbi83qevngpgs2j500fgc8gpt9u.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent.parent.parent, "client_secret.json")

github_blueprint = make_github_blueprint(client_id='40beae0bb8dc9068fa01', client_secret='02b1fcc230bd3a4208c096669aa1003edeaee8c1')
auth_bp.register_blueprint(github_blueprint, url_prefix='/github_login')
discord_client = APIClient(token='MTIxMTcxMzY3NDMzMTU1Nzk3OQ.GTZ9M5.1BA9pDnVz3pUibIc_2eefopXWp6LxzLGDyGOXQ', client_secret='VngLCKNaf5FoUi_bxO1GaMLFbMRWHgvx')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

google_flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file,
                                     scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
                                     redirect_uri="http://127.0.0.1:5000/callback")


@auth_bp.route("/logout")
@login_required
def handle_logout():
    user_id = current_user.get_id()
    if user_id in online_users:
        online_users.remove(user_id)
    logout_user()
    return render_template('index.html')


@auth_bp.route("/login", methods=['GET', 'POST'])
def handle_login():
    if request.method == 'POST':
        user = logic.user_auth(request.form['email'], request.form['password'])
        if user is None:
            flash('Неверный логин/пароль', 'error')
            return render_template('login.html')
        user_login = UserLogin().create(user)
        login_user(user_login)
        return redirect(f"/profiles/{user.user_id}")
    return render_template('login.html')


@auth_bp.route("/registration", methods=["POST", "GET"])
def handle_register():
    if request.method == 'POST':
        response = logic.user_register(request.form.copy())
        flash(*response)
    return render_template("registration.html")


@auth_bp.route("/login_google", methods=['GET', 'POST'])
def handle_login_google():
    authorization_url, state = google_flow.authorization_url()
    sess['state'] = state
    return redirect(authorization_url)


@auth_bp.route("/login_github", methods=['GET', 'POST'])
def handle_login_github():
    if not github.authorized:
        return redirect(url_for('auth.github.login'))
    id_info = github.get('/user')
    if id_info.ok:
        id_info = id_info.json()
        user = logic.user_auth_by_service(id_info['login'])
        if user is None:
            user = logic.user_auth_by_service(id_info['email'])
        if user is None:
            if 'email' in id_info.keys() and id_info['email'] is not None:
                email = id_info['email']
            else:
                email = id_info['html_url']
            logic.user_register_by_service(email, id_info['login'], id_info['avatar_url'])
            user = logic.user_auth_by_service(id_info['email'])
        user_login = UserLogin().create(user)
        login_user(user_login)
        return redirect(f"/profiles/{user.user_id}")
    return render_template('index.html')


@auth_bp.route("/login_discord", methods=['GET', 'POST'])
def handle_login_discord():
    return redirect('https://discord.com/oauth2/authorize?client_id=1211713674331557979&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fcallback_discord&scope=identify+email')


@auth_bp.route("/callback")
def handle_callback():
    google_flow.fetch_token(authorization_response=request.url)

    if not sess['state'] == request.args["state"]:
        return render_template('index.html')

    credentials = google_flow.credentials
    request_session = requests.Session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    id_info = id_token.verify_oauth2_token(id_token=credentials._id_token, request=token_request,
                                           audience=GOOGLE_CLIENT_ID)
    user = logic.user_auth_by_service(id_info['email'])
    if user is None:
        logic.user_register_by_service(id_info['email'], id_info['email'], id_info['picture'])
        user = logic.user_auth_by_service(id_info['email'])
    user_login = UserLogin().create(user)
    login_user(user_login)
    return redirect(f"/profiles/{user.user_id}")


@auth_bp.route("/callback_discord", methods=['GET', 'POST'])
def handle_callback_discord():
    code = request.args['code']
    access_token = discord_client.oauth.get_access_token(code, 'http://127.0.0.1:5000/callback_discord').access_token
    bearer_client = APIClient(access_token, bearer=True)
    cur_user = bearer_client.users.get_current_user()
    print(cur_user, type(cur_user))
    user = logic.user_auth_by_service(cur_user.email)
    if user is None:
        user = logic.user_auth_by_service(cur_user.username)
    if user is None:
        logic.user_register_by_service(cur_user.email, cur_user.username, cur_user.avatar_url)
        user = logic.user_auth_by_service(cur_user.email)
    user_login = UserLogin().create(user)
    login_user(user_login)
    return redirect(f"/profiles/{user.user_id}")