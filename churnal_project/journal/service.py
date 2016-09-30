from datetime import timedelta


def get_date_list(start_date, num_days):
    date_list = [start_date - timedelta(days=x) for x in range(0, num_days)]

    return date_list
