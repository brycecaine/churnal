from oauth2client import client
from django.http import HttpResponse
from django.shortcuts import redirect, render
# from oauth2client.client import OAuth2WebServerFlow

import os

GDATA_CLIENT_ID = os.environ['GDATA_CLIENT_ID']
GDATA_CLIENT_SECRET = os.environ['GDATA_CLIENT_SECRET']

def oauth(request):
    flow = client.OAuth2WebServerFlow(
        client_id=GDATA_CLIENT_ID,
        client_secret=GDATA_CLIENT_SECRET,
        scope='https://www.googleapis.com/auth/drive.readonly',
        redirect_uri='http://127.0.0.1:8000/oauth2callback')

    if 'code' not in request.GET:
        auth_uri = flow.step1_get_authorize_url()

        return redirect(auth_uri)

    else:
        auth_code = request.GET.get('code')
        credentials = flow.step2_exchange(auth_code)
        request.session['creds7'] = credentials.to_json()

        return redirect('/journal')
