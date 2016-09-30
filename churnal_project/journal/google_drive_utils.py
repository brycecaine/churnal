from apiclient import discovery
from apiclient.http import MediaIoBaseDownload
from datetime import datetime, timedelta
from dateutil.parser import parse
from django.shortcuts import redirect
from oauth2client import client
from operator import itemgetter

import frontmatter
import httplib2
import io
import urllib2

# Keep following https://developers.google.com/api-client-library/python/guide/aaa_oauth
# and https://developers.google.com/picasa-web/docs/2.0/developers_guide_protocol
# django google api ref: https://developers.google.com/api-client-library/python/guide/django
# Search google drive files: https://developers.google.com/drive/v3/web/search-parameters


def get_drive_service(creds):
    drive_service = None
    if creds:
        credentials = client.OAuth2Credentials.from_json(creds)

        if not credentials.access_token_expired:
            http_auth = credentials.authorize(httplib2.Http())
            drive_service = discovery.build('drive', 'v3', http_auth)

    return drive_service


def get_folder(drive_service, gd_path):
    folder_id = None

    if gd_path:
        path_list = gd_path.split('/')
        del path_list[0]

        folder_id = 'root'

        for element in path_list:
            query = ("""
                mimeType = 'application/vnd.google-apps.folder' and
                '%s' in parents and
                name = '%s'""" % (folder_id, element))
            results = drive_service.files().list(q=query).execute()
            folder_id = results['files'][0]['id']

    return folder_id


def get_children(drive_service, folder_id, kind, entry_date):
    file_list = []

    mimetype_match = ''

    if kind == 'text':
        mimetype_match = 'text/'
    elif kind == 'image':
        mimetype_match = 'image/jpeg'

    next_date = entry_date + timedelta(days=1)

    name_date_match = entry_date.strftime('%Y-%m-%d')
    mod_time_match_from = entry_date.strftime('%Y-%m-%dT%H:%M:%S')
    mod_time_match_to = next_date.strftime('%Y-%m-%dT%H:%M:%S')

    print('+++++++++++++++++++++++++')
    print(mimetype_match, name_date_match, mod_time_match_from, mod_time_match_to, folder_id)

    files_query = ("""
        trashed = false and
        mimeType contains '%s' and
        (name contains '%s' or
          (modifiedTime > '%s' and modifiedTime < '%s')) and
        '%s' in parents""" % (mimetype_match, name_date_match, mod_time_match_from, mod_time_match_to, folder_id))
    try:
        children = drive_service.files().list(q=files_query).execute()

        file_list = sorted(
            children.get('files', []), key=itemgetter('name'), reverse=True)

    except (urllib2.HTTPError, AttributeError):
        pass

    return file_list


def get_raw_files(drive_service, file_list):
    raw_files = []
    for file_item in file_list:
        req = drive_service.files().get_media(fileId=file_item.get('id'))
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, req)
        done = False

        while done is False:
            status, done = downloader.next_chunk()

        raw_files.append(fh.getvalue())

    return raw_files


def get_entries(drive_service, file_list):
    entries = []

    raw_files = get_raw_files(drive_service, file_list)

    for raw_file in raw_files:
        entries.append(frontmatter.loads(raw_file))

    return entries


def get_photos(drive_service, file_list):
    photos = []

    raw_files = get_raw_files(drive_service, file_list)

    for raw_file in raw_files:
        print('PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP')
        print(raw_file)

    return photos
