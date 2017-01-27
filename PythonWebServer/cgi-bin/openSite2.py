#! /usr/bin/python
import cgi, cgitb, siteUtilities, forumUtilities
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
        if userID.isdigit():
            userID = int(userID)
        else:
            userID = -1
    else:
        userID =-1
    if "isForum" in form and "category" in form:
        forumContents = form.getvalue("isForum") #the txt version of it WITH NO FILE EXTENSION
        category = form.getvalue("category")
        toSite = forumUtilities.threadHTML(forumContents, category,userID)
    else:
        if "toSite" in form:
            toSite = extractHTML(PATH + form.getvalue("toSite"))                                 
    if toSite=="":
        showError()
    else:
        toSite = siteUtilities.insertPost4(toSite,"<form ", "</form>", "<input type = hidden name = userID value = %d>"%(userID))
        print toSite
def showError():
    print HTML_HEADER2
    print "you goofed"
    print "</body></html>"
    #Error code here. INCLUDE HTML HEADER2!!!!!
def extractHTML(filename):
    try:
            f = open(filename,"rU")
            s  = f.read()
            f.close()
            return s
    except:
            return ""

        
main()

