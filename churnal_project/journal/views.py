from apiclient import discovery
from apiclient.http import MediaIoBaseDownload
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from oauth2client import client
from operator import itemgetter
from journal import service

import httplib2
import io
import json
import pprint
import requests

# Keep following https://developers.google.com/api-client-library/python/guide/aaa_oauth
# and https://developers.google.com/picasa-web/docs/2.0/developers_guide_protocol
# django google api ref: https://developers.google.com/api-client-library/python/guide/django
# Search google drive files: https://developers.google.com/drive/v3/web/search-parameters
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

	path = '/journals/gen_00/bryce_eryn_caine/blog/_posts'
	folder_id = service.get_folder(credentials, path)

	# ---------------------------------------------------------------------
	# Get children of folder
	# children = drive_service.children().list(folderId=folder_id).execute()
	children = drive_service.files().list(q="'%s' in parents and mimeType contains 'text/' and trashed = false" % folder_id).execute()

        # file_list = sorted(children.get('files', []), reverse=True)
	file_list = sorted(children.get('files', []), key=itemgetter('name'), reverse=True)

        for file in file_list:
            # Process change
            print 'Found file: %s (%s)' % (file.get('name'), file.get('id'))

	print('children')
	pp.pprint(children)

	# ---------------------------------------------------------------------
	# Get file id
	file_id = file_list[0].get('id')

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
