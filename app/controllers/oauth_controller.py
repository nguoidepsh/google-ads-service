from authlib.integrations.starlette_client import OAuth
from settings import CLIENT_ID, CLIENT_SECRET

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorize_params={'access_type': 'offline', 'prompt': 'consent' },
    client_kwargs={
        'scope': 'email openid profile https://www.googleapis.com/auth/adwords',
        'redirect_url': 'http://localhost:8000/auth'
    }
)
