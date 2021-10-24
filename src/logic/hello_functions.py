from urllib.parse import urlparse
from datetime import date
import logging, json
from db.db import *

def get_user_and_validate_path(path):
    #ignoring querry parameters
    requesturl = urlparse(path)
    pathlist = requesturl.path.split("/")
    logging.debug("path after splitting : %s ", " ".join(pathlist))
    #only serving /hello/<username> where username is alpha , if valid return username
    if ( len(pathlist) == 3 and pathlist[1] == "hello" and pathlist[2].isalpha()):
        return pathlist[2]
    elif ( len(pathlist) == 2 and pathlist[1] == "health" ):
        return "200"
    else:
        return -1

def get_birthday_response(user):
    response = {}
    code = 0
    try:
        dob = get_dob(user)[0][0]
        today = date.today()
        logging.debug("got user %s with dob %s and today is %s", user, dob, today)
        days = 0
        if ( dob.month == today.month and dob.day == today.day ):
            response["message"] = ("Hello, %s! Happy Birthday!" % user)
        elif ( dob.month == 2 and dob.day == 29 ):
            # could modify to be celebrated on the 28th of feb or the first of march on non-bisect years
            years_to_bisect = 4 - ( today.year % 4 )
            if ( years_to_bisect == 4 and today < date(today.year, dob.month, dob.day) ):
                days = (date(today.year, dob.month, dob.day) - today).days
            else: 
                days = (date(today.year + years_to_bisect, dob.month, dob.day) - today).days
            logging.debug('Calculated days until bisect birthday %d', days)
            response["message"] = ("Hello, %s! Your birthday is in %d day(s)" % (user, days))
        else:
            if ( today < date(today.year, dob.month, dob.day) ):
                days = (date(today.year, dob.month, dob.day) - today).days
            else: 
                days = (date(today.year + 1, dob.month, dob.day) - today).days
            logging.debug('Calculated days until birthday %d', days)
            response["message"] = ("Hello, %s! Your birthday is in %d day(s)" % (user, days))
        code = 200
    except psycopg2.OperationalError as err:
        logging.debug('Database operational error') 
        code = 503  
    except IndexError as err:         
        logging.debug('User does not exist')
        code = 404
    return (code,response)


def upsert_and_validate_json(user,put_body):
    code = 0
    try:
        #Validate data is json 
        body = json.loads(put_body)
        try:
            #Validate dateOfBirth it's an actual date
            birthdate = date.fromisoformat(body['dateOfBirth'])
            #Verify it's at least one day in the past
            if ( date.today() <= birthdate ):
                code = 400
                logging.debug('Data error : dob is not in the past')
            else:
                try:
                    # add/modify dob 
                    upsert_dob(user,birthdate.strftime('%Y-%m-%d'));
                    code = 204
                    logging.debug("adding user %s with dob %s", user, birthdate.strftime('%Y-%m-%d'))
                except psycopg2.OperationalError as err:
                    code = 503
                    logging.debug('Database operational error')
        except (ValueError, KeyError) as err:
            code = 400
            logging.debug('Data error : dob is not a valid date')
    except ValueError as err:
        code = 411
        logging.debug('Request data missing or invalid json')
    return code