from apiclient import discovery
from apiclient.http import MediaIoBaseDownload
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from oauth2client import client

import httplib2
import io
import json
import pprint
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
	# ---------------------------------------------------------------------
        # Setup
        http_auth = credentials.authorize(httplib2.Http())
        drive_service = discovery.build('drive', 'v3', http_auth)
	pp = pprint.PrettyPrinter(indent=4)

	# ---------------------------------------------------------------------
	# Get folder
	print(999)
	# files = drive_service.files().list(q='name="journals"').execute()


	results = drive_service.files().list(q="'root' in parents and mimeType = 'application/vnd.google-apps.folder' and name = 'journals'").execute()
	pp.pprint(results)

	folder_id = results['files'][0]['id']

	query = "'%s' in parents and name = 'gen_00' and mimeType='application/vnd.google-apps.folder'" % folder_id
	results = drive_service.files().list(q=query).execute()
	pp.pprint(results)

	# ---------------------------------------------------------------------
	# Get children of folder
	# children = drive_service.children().list(folderId=folder_id).execute()
	# pp.pprint(children)

	# ---------------------------------------------------------------------
	# Get file id
        file_id = '0B8I9wVZNPA_ZUzVORnd4RHJmdzA'

	# ---------------------------------------------------------------------
	# Get contents of file
        req = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, req)
        done = False

        while done is False:
            status, done = downloader.next_chunk()
            print "Download %d%%." % int(status.progress() * 100)

        entry = fh.getvalue()

        return render(request, 'index.html', locals())
