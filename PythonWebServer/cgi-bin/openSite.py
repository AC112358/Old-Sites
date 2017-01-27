#! /usr/bin/python
import cgi, cgitb, forumUtilities, accountUtilities, linkToForumHome
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
    try:
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
                try:
                    forumContents=form.getvalue("userPost")
                    postBool = True
                    postVal = accountUtilities.parseUserInfo(userID).get("POST",["1"])[-1]
                    morePost = ""
                    errormessage = ""
                    #print "THIS IS POST VAL: " + postVal
                    if type(postVal) == type("") and "</font>" in postVal and "in FORUM: " in postVal:
                        try:
                            morePost = postVal[postVal.rfind(" in FORUM: ")+11:postVal.rfind(" in CATEGORY: ")]
                            postVal = postVal[postVal.find("</font>")+9:postVal.rfind(" in FORUM: ")]
                        except:
                            postVal = ""
                    #print "THIS IS POST VAL:" + postVal + "."
                    #print "THIS IS FORUMCONTENTS:" + forumContents + "."
                    if postVal==forumContents and morePost==forumName:
                        postBool = False
                    #print postBool
                    if postBool and "".join(forumContents.split())!="":
                        forumContents=forumUtilities.makePost(users[userID].get("uname","unknown user"), users[userID].get("status","guest"),forumContents)
                        #print "HERE ARE THE FORUM CONTENTS " + forumContents
                        #print userID
                        #print accountUtilities.addToUserInfo("\nPOST", " in FORUM: %s in CATEGORY: %s", userID)
                        forumContents = "<br>".join(forumContents.split("\n"))
                        accountUtilities.addToUserInfo("\nPOST", forumContents + " in FORUM: %s in CATEGORY: %s"%(forumName, category), userID)
                        forumUtilities.post(forumContents,forumName, category)
                        #print forumUtilities.threadHTML(forumName, category,userID)
                    #print forumUtilities.threadHTML(forumName, category,userID) + "OK THATS IT<br><br><br>"
                except:
                    print "Post could not be made due to an error while testing if it had already been posted. "
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
            %s
            <input type = submit value = Back>
            </form>'''%(back)
        if not ("toSite" in form and form.getvalue("toSite")=="forumHome.html"):
            toSite+='''
                <form method = get action = openSite.py>
                <input type = hidden name = toSite value = forumHome.html>
                <input type = submit value = "Forum Home">
                </form>'''
        if toSite=="":
            showError()
        else:
            if "<input type = hidden name = userID" not in toSite:
                toAdd = '''
                <input type = hidden name = userID value = %d>
                '''%(userID)
                #YOU CAN ADD TO TOADD IF YOU WANT TO CREATE MORE BACK BUTTONS
                toSite = toSite.replace("</form>", "%s\n</form>"%(toAdd))
        """if "<input type = hidden name = userID" not in toSite:
            toSite = toSite.replace("</form>", "<input type = hidden name = userID value = %d>\n</form>"%(userID))"""
        print toSite
    except:
        print HTML_HEADER
        print HTML_HEADER2
        print "An unknown error occured!"
        print "</body></html>"
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
    print "Site not specified. Try refreshing or going back to the previous page."
    print "</body></html>"
    #Error code here. INCLUDE HTML HEADER2!!!!!

main()
