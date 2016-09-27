from apiclient import discovery

import httplib2

def get_folder(credentials, path):
    http_auth = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http_auth)

    path_list = path.split('/')
    del path_list[0]

    folder_id = 'root'

    for element in path_list:
	query = "'%s' in parents and mimeType = 'application/vnd.google-apps.folder' and name = '%s'" % (folder_id, element)
	results = drive_service.files().list(q=query).execute()
	folder_id = results['files'][0]['id']

    return folder_id
