from datetime import datetime
from dateutil.parser import parse
from django.shortcuts import redirect, render
from journal import google_drive_utils, service


def index(request):

    return render(request, 'index.html', locals())


def setpath(request):
    # Ask user for path (guided)
    # Store path in GoogleUser
    return render(request, 'set_path.html', locals())


def timeline(request):
    date_list = service.get_date_list(datetime.today(), 5)

    return render(request, 'timeline.html', locals())


def day(request, day=None):
    creds = request.session.get('creds7')
    drive_service = google_drive_utils.get_drive_service(creds)

    if drive_service:
        entry_date = parse(day)
        gd_path = '/journals/gen_00/bryce_eryn_caine'
        gp_path = '/Google Photos/2016'

        gd_folder_id = google_drive_utils.get_folder(drive_service, gd_path)
        gd_file_list = google_drive_utils.get_children(drive_service, gd_folder_id, 'text', entry_date)
        g_entries = google_drive_utils.get_entries(drive_service, gd_file_list)

        gp_folder_id = google_drive_utils.get_folder(drive_service, gp_path)
        gp_file_list = google_drive_utils.get_children(drive_service, gp_folder_id, 'image', entry_date)
        # Find a better way. probably picasa api directly
        g_photos = google_drive_utils.get_photos(drive_service, gp_file_list)

        return render(request, 'day.html', locals())

    else:
        return redirect('/oauth2callback')
