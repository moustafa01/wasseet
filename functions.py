from flask import session

def check_if_active():
    if (session["isactivated"] == True):
        return True
    else:
        return False
