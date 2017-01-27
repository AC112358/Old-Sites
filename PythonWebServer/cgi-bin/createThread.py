#! /usr/bin/python
import cgi, cgitb, os, forumUtilities
cgitb.enable()
HTML_HEADER="Content-type:text/html\n"
HTML_END = "</body>\n</html>"

def main():
    form = cgi.FieldStorage()
    print HTML_HEADER
    print "<html><head></head>\n<body>\n"
    userID =-1
    threadName=""
    category=""
    proceed = True
    if proceed and "userID" in form and type(form.getvalue("userID"))==type("") and form.getvalue("userID").isdigit():
        userID=int(form.getvalue("userID"))
    else:
        notEnoughInfo("the site did not receive user information. Try signing in or signing up.")
        proceed= False
    if proceed and "threadName" in form and form.getvalue("threadName")!="Default Thread Name - NO underscores allowed":
        threadName=form.getvalue('threadName')
    else:
        notEnoughInfo("the thread name was nonexistent or still had the default name ('Default Thread Name...').")
        proceed = False
    if proceed and "category" in form:
        category=form.getvalue("category")
    else:
        notEnoughInfo("the category name was not specified.")
        proceed = False
    #NOTE that this will print all existent errors in user input
    if not proceed:
        print HTML_END
    else:
        main2(userID, threadName, category)
        print HTML_END
        
def main2(userID, threadName, category):
    #proceed = True
    try:
        if "_" in threadName:
            notEnoughInfo("underscores aren't allowed in thread names. They are used to replace spaces in files.")
            return
        allCategories = os.listdir("Saved_Threads/")
        allCategories = [os.listdir("Saved_Threads/"+i) for i in os.listdir("Saved_Threads")]
        #print "hi"
        for j in allCategories:
            for k in j:
                if processString(threadName)==processString(k[:-4]):
                    notEnoughInfo("a thread with the same or a very similar name (%s) exists on the forum."%(" ".join(k.split("_"))))
                    return
        if forumUtilities.makeThread(threadName, category):
            if firstLine(userID,threadName, category)==True:
                print "Thread successfully created!"
            else:
                print "The first line of the forum containing extra information could not be added. The thread was still created."
        else:
            notEnoughInfo("something went wrong when the thread was being saved. This could be due to someone else trying to make a thread of the same name or something went wrong with permissions or the server.")
       # print "hi at the end"
    except:
        notEnoughInfo("something went wrong on the server.")
    
def notEnoughInfo(lacks):
    print "<br>Thread could not be added because " + lacks
def processString(s):
    s = s.lower()
    s = " ".join(s.split("_"))
    total = ""
    thelist = []
    for i in s:
        if i not in "!.: \t\n":
            total+=i
        else:
            if total!="":
                thelist.append(total)
                total = ""
    if total!="":
        thelist.append(total)
    return thelist
def firstLine(userID,threadName, category):
    import datetime, accountUtilities
    threadName = "_".join(threadName.split(" "))
    category = "_".join(category.split(" "))
    today = datetime.date.today()
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    timeInfo = "%s %d, %d" %(months[today.month-1],today.day,today.year)
    users = accountUtilities.masterDict("userInfo.txt")
    if userID in users:
        timeInfo = "<i>Created by %s on %s</i><br>"%(users[userID].get("uname", "Guest"), timeInfo)
    else:
        timeInfo = "<i>Created by Guest on %s</i><br>"%(timeInfo) 
    #print timeInfo
    return forumUtilities.addToThread(threadName, category,timeInfo)
def addToTop(threadName, category, message):
    category = "_".join(category.split(" "))
    threadName = "_".join(threadName.split(" "))
    if ".txt" not in threadName[-4:]:
        threadName+=".txt"
    try:
        path = "Saved_Threads/%s/%s"%(category,threadName)
        if os.path.exists(path):
            f = open(path, "rU")
            s = f.read()
            f.close()
            f = open(path, "w")
            f.write(message+"\n")
            f.write(s)
            f.close()
            return "Line successfully added to top!"
        else:
            return "Line could not be added to top because the file doesn't exist."
    except:
        return "An error occured when saving the file."

main()

#main()
