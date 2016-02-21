from apiclient import discovery
from apiclient.http import MediaIoBaseDownload
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from oauth2client import client

import httplib2
import io
import json
import requests

# Keep following https://developers.google.com/api-client-library/python/guide/aaa_oauth
# and https://developers.google.com/picasa-web/docs/2.0/developers_guide_protocol
# django google api ref: https://developers.google.com/api-client-library/python/guide/django
def index(request):
    if 'creds7' not in request.session:

        return redirect('/oauth2callback')

    credentials = client.OAuth2Credentials.from_json(request.session['creds7'])

    if credentials.access_token_expired:

        return redirect('/oauth2callback')

    else:
        http_auth = credentials.authorize(httplib2.Http())
        drive_service = discovery.build('drive', 'v3', http_auth)
        # files = drive_service.files().list(q='name="Djangocon notes"').execute()

        file_id = '0B8I9wVZNPA_ZUzVORnd4RHJmdzA'
        req = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, req)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print "Download %d%%." % int(status.progress() * 100)

        entry = fh.getvalue()

        return render(request, 'index.html', locals())
