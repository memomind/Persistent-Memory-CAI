from datetime import datetime

def normalize_date(date:str):
    date_obj = datetime.fromisoformat(date).date()
    date = date_obj.strftime('%Y-%m-%d')
    return date

def normalize_name(name:str):
    pass