from authlib.integrations.flask_client import OAuth
import os

oauth = OAuth()


def init_app(application):
    oauth.init_app(application)


auth0 = oauth.register(
    "auth0",
    client_id=os.environ["AUTH0_ID"],
    client_secret=os.environ["JWT_CODE_SIGNING_SECRET"],
    api_base_url="https://" + os.environ["AUTH0_DOMAIN"],
    access_token_url="https://" + os.environ["AUTH0_DOMAIN"] + "/oauth/token",
    authorize_url="https://" + os.environ["AUTH0_DOMAIN"] + "/authorize",
    client_kwargs={
        "scope": "openid profile email",
    },
)

signup_auth0 = oauth.register(
    "signup_auth0",
    client_id=os.environ["AUTH0_ID"],
    client_secret=os.environ["JWT_CODE_SIGNING_SECRET"],
    api_base_url="https://" + os.environ["AUTH0_DOMAIN"],
    access_token_url="https://" + os.environ["AUTH0_DOMAIN"] + "/oauth/token",
    authorize_url="https://" +
    os.environ["AUTH0_DOMAIN"] + f"/authorize?screen_hint=signup",
    client_kwargs={
        "scope": "openid profile email",
    },
)
