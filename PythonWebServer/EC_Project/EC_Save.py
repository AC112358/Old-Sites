#! /usr/bin/python
import cgi, cgitb
cgitb.enable()
import EC_ProcessFile
def floatConvert(takeIn):
    try:
        float(takeIn)
        return True
    except:
        return False
def saveGame(username,gameName,score,level):
    games = EC_ProcessFile.makeGameDict()
    proceed = True
    if username in games:
        if gameName in games[username]:
            proceed = True
    if not proceed:
        return "Username &/or save slot not recognized. Game could not be saved."
    games[username][gameName]["score"] = score
    games[username][gameName]["level"]=level
    if EC_ProcessFile.writeGameDict(games):
        return "Successfully saved progress!"
    else:
        return "Unable to save progress due to an error with the program."
def main():
    form = cgi.FieldStorage()
    username = ""
    response = ""
    if "username" in form:
        username = form.getvalue("username")
    if "saveGame" in form and "score" in form and "level" in form:
        s = form.getvalue("score")
        l = form.getvalue("level")
        if floatConvert(s) and floatConvert(l):
            response = saveGame(username,form.getvalue("saveGame"), float(s), float(l))
main()
