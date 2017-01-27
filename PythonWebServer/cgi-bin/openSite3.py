#! /usr/bin/python
import cgi, cgitb, siteUtilities, forumUtilities, accountUtilities, linkToForumHome
cgitb.enable()
HTML_HEADER = "Content-type: text/html\n"
HTML_HEADER2 = '''
<html>
<head></head>
<body>
'''
"""<input type = hidden toSite = <toSite.html>>"""
PATH=""
def main():
    print HTML_HEADER
    form = cgi.FieldStorage()
    toSite = ""
    userID = ""
    if "userID" in form:
        userID = form.getvalue("userID")
        if type(userID)==type("") and userID.isdigit():
            userID = int(userID)
        else:
            userID = -1
    else:
        userID =-1
    if "isForum" in form and "category" in form:
        forumName = form.getvalue("isForum") #the txt version of it WITH NO FILE EXTENSION
        users = accountUtilities.masterDict("userInfo.txt")
        category = form.getvalue("category")
        if "userPost" in form and userID in users:
            forumContents=form.getvalue("userPost")
            forumContents=forumUtilities.makePost(users[userID].get("uname","unknown user"), users[userID].get("status","guest"),forumContents)
            #print "HERE ARE THE FORUM CONTENTS " + forumContents
            accountUtilities.addToUserInfo("POST", forumContents, userID)
            forumUtilities.post(forumContents,forumName, category)
            #print forumUtilities.threadHTML(forumName, category,userID)
        toSite += forumUtilities.threadHTML(forumName, category,userID)
    else:
        if "toSite" in form:
            toSite = extractHTML(PATH + form.getvalue("toSite"), userID) 
    if "fromSite" in form:
        back = form.getvalue("fromSite")
    if "fromCategory" in form:
        back = "<input type = hidden name = isForum value = %s>\n<input type = hidden name = category value =%s>"%(back, form.getvalue("fromCategory"))
    else:
        back = "<input type=hidden name=toSite value=%s>"%(back)
    toSite+='''
    <form method = get action = openSite.py>
    <input type = hidden name = userID value = %d>
    %s
    <input type = submit value = Back>
    </form>'''%(userID,back)                       
    if toSite=="":
        showError()
    else:
        #toSite = siteUtilities.insertPost4(toSite,"<form ", "</form>", "<input type = hidden name = userID value = %d>"%(userID))
    if "<input type = hidden name = userID" not in toSite:
            toSite = toSite.replace("</form>", "<input type = hidden name = userID value = %d>\n</form>"%(userID))
    print toSite
def extractHTML(filename, userID):
    if filename=="forumHome.html":
            return linkToForumHome.main2(userID)
    try:
            f = open(filename,"rU")
            s  = f.read()
            f.close()
            return s
    except:
            return ""
def showError():
    print HTML_HEADER2
    print "you goofed"
    print "</body></html>"
    #Error code here. INCLUDE HTML HEADER2!!!!!

main()
