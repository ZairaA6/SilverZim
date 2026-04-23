import json
RECORDS_FILE = "finalnearecords.json"

def save_data(nickname, all_time_saved):
    data = {'nickname': nickname, 'all time score': all_time_saved}  # creates a data entry for the json file

    with open(RECORDS_FILE, 'a') as file:                  # saves data entry to json file
       json.dump(data, file)
       file.write('\n')

def load_records():
    try:
        with open(RECORDS_FILE, 'r') as file:             
           lines = reversed(file.readlines())                       # reversed() is used so that most recent update for the user_nickname can be read first
           user_records = [json.loads(line) for line in lines]
           return user_records
    except FileNotFoundError:                                       # vaidating for errors
        return []

def get_user_score(nickname, all_user_records):
    for record in all_user_records:
        if record['nickname'] == nickname:
                view_user_score = record['all time score']
                return view_user_score
    return None