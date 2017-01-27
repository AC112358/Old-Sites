#! /usr/bin/python
import os, accountUtilities, forumUtilities
import cgi, cgitb
cgitb.enable()
#import pdb
#pdb.set_trace()
cgitb.enable()
#each function is a different component to the staff capabilities
def main():
    print "Content-type: text/html\n"
    print "<html><head><link rel = http://marge.stuy.edu/~ricky.chen/foxy.css></head>\n<body>"
    form = cgi.FieldStorage()
    allFuncts = {"addCategory":addCategory,"promoteUser":promoteUser, "viewMessages":viewMessages,"sendMessage":sendMessage,"demoteUser":demoteUser, "seeReports":seeReports, "closeThread":closeThread,"seeUserPosts":seeUserPosts, "makeReportThread":makeReportThread}
    if "runFunction" in form:
        functionToRun = form.getvalue("runFunction")
        if "inputs" in form: #NOTE THAT WE EXPECT A STRING OR A LIST HERE
            inputs = form.getvalue("inputs")
            userID = -1
            if "userID" in form:
                userID = form.getvalue("userID")
                if type(userID)==type("") and userID.isdigit():
                    userID = int(userID)
                else:
                    userID =-1
            users = accountUtilities.masterDict("userInfo.txt")
            #print str(users) + "<br>"
            proceed = True
            userDict = {}
            if userID in users:
                userDict = users[userID]
            else:
                print "Your account isn't recognized by the control panel. Make sure you're signed in."
                proceed = False
            if proceed:
                if type(inputs)!=type([]) and type(inputs)!=type((2,3)):
                    inputs = [inputs]
                elif type(inputs)==type((2,3)):
                    inputs = list(inputs)
                else:
                    for i in range(len(inputs)):
                        inputs[i] = str(inputs[i])
                if functionToRun in allFuncts:
                    #print "Function is being called!"
                    allFuncts[functionToRun](userDict,inputs)
                else:
                    print "The function called is not valid."
        else:
            print "Not enough information sent for the function to be performed. Make sure all forms are filled in."
    else:
        print "No request sent!"
    print '''<form method = get action = openSite.py>
            <input type = hidden name = toSite value = forumHome.html>
            <input type = submit value = "Forum Home">
            </form>'''
    print "</body></html>"
def main2(form):
    print "Content-type:text/html\n"
    print "<html>\n<body>"
    #form = cgi.FieldStorage()
    allFuncts = {"addCategory":addCategory,"promoteUser":promoteUser, "makeReportThread":makeReportThread,"demoteUser":demoteUser, "seeReports":seeReports, "closeThread":closeThread,"seeUserPosts":seeUserPosts}
    if "runFunction" in form:
        functionToRun = form.get("runFunction","")
        if "inputs" in form: #NOTE THAT WE EXPECT A STRING OR A LIST HERE
            inputs = form.get("inputs","")
            userID = -1
            if "userID" in form:
                userID = form.get("userID","")
                #print userID
                if type(userID)==type("") and userID.isdigit():
                    userID = int(userID)
                else:
                    userID =-1
            users = accountUtilities.masterDict("userInfo.txt")
            proceed = True
            userDict={}
            if userID in users:
                userDict = users[userID]
            else:
                print "Your account isn't recognized by the control panel. Make sure you're signed in."
                proceed = False
            if proceed:
                if type(inputs)!=type([]) and type(inputs)!=type((2,3)):
                    inputs = [inputs]
                elif type(inputs)==type((2,3)):
                    inputs = list(inputs)
                else:
                    for i in range(len(inputs)):
                        inputs[i] = str(inputs[i])
                if functionToRun in allFuncts:
                    allFuncts[functionToRun](userDict,inputs)
                else:
                    print functionToRun
                    print "not recognized"
    print "</body></html>"
def addCategory(userDict, inputList): #MAKE SURE INPUTLIST LONG ENOUGH
    if len(inputList)<1:
        print "Not enough input for this function!"
        return 
    category = inputList[0]
    status = userDict.get("status", "guest")
    if meetsReqs(status,"admin")>=0:
        x = forumUtilities.addCategory(category)
        if x==0:
            print "Category %s successfully added!"%(category)       
        elif x==2:
            print "A similar category name already exists."
        elif x==3:
            print "This action could not be completed because the directory was being modified."
        else:
            print "This action could not be completed due to a server error."
    else:
        print "Sorry, this action can only be performed by Admins+."
def promoteUser(userDict, inputList):
    if len(inputList)<1:
        print "Not enough input for this function!"
        return
    username = inputList[0]
    status = userDict.get("status", "guest")
    statuses = ["guest","member","moderator","admin", "owner"]
    diff = meetsReqs(status,"admin")
    if diff>=0:
        users =accountUtilities.masterDict("userInfo.txt")
        for i in users.keys():
            if users[i].get("uname", "member")==username:
                if meetsReqs(status, users[i].get("status", "member"))>0:
                    if status in statuses and users[i].get("status", "member") in statuses:
                        if statuses.index(users[i].get("status", "member"))<len(statuses)-1:
                            users[i]["status"] = statuses[statuses.index(users[i].get("status", "member"))+1]
                            #print users[i]["status"]
                            #print users
                            if accountUtilities.writeDict(users,"userInfo.txt"):
                                print "Successfully promoted user.<br>"
                                if "id" in userDict:
                                    accountUtilities.addToUserInfo("ACTIVITY","%s: %s has promoted %s to %s."%(makeTimeStamp(),userDict.get("uname",""), users[i].get("uname",""), users[i].get("status","")),userDict["id"])
                            else:
                                print "Unable to promote user because the file is inaccessible.<br>"
                        else:
                            print "The user's rank was the highest possible.<br>"
                    else:
                        print "The site couldn't recognize a status given.<br>"
                else:
                    print "Sorry, that user doesn't have a lower rank than you, so you can't promote them.<br>"
                break
        else:
            print "User " + username + " could not be found."
    else:
        print "Sorry, this action can only be performed by Admins+."
def demoteUser(userDict, inputList):
    if len(inputList)<1:
        print "Not enough input for this function!"
        return
    username = inputList[0]
    status = userDict.get("status", "guest")
    statuses = ["guest","member","moderator","admin", "owner"]
    diff = meetsReqs(status,"admin")
    if diff>=0:
        users =accountUtilities.masterDict("userInfo.txt")
        for i in users.keys():
            if users[i].get("uname", "member")==username:
                if meetsReqs(status, users[i].get("status", "member"))>0:
                    if status in statuses and users[i].get("status", "member") in statuses:
                        if statuses.index(users[i].get("status", "member"))>0:
                            users[i]["status"] = statuses[statuses.index(users[i].get("status", "member"))-1]
                            #print users[i]["status"]
                            #print users
                            if accountUtilities.writeDict(users,"userInfo.txt"):
                                print "Successfully demoted user."
                                if "id" in userDict:
                                    accountUtilities.addToUserInfo("ACTIVITY","%s: %s has promoted %s to %s."%(makeTimeStamp(),userDict.get("uname",""), users[i].get("uname",""), users[i].get("status","")),userDict["id"])
                            else:
                                print "Unable to demote user because the file is inaccessible.<br>"
                        else:
                            print "The user's rank was the lowest possible.<br>"
                    else:
                        print "The site couldn't recognize a status given.<br>"
                else:
                    print "Sorry, that user doesn't have a lower rank than you, so you can't demote them.<br>"
                break
        else:
            print "User " + username + " could not be found."
    else:
        print "Sorry, this action can only be performed by Admins+."
def meetsReqs(userStatus, req):
    statuses = ["guest", "member","moderator","admin", "owner"]
    if req in statuses:
        return statuses.index(userStatus) - statuses.index(req)
    return -1
#THIS IS JUST WORKING WITH THE STAFFCHAT DIRECTORY IN SAVED_THREADS
#SO JUST MAKE A SUBMIT BUTTON TO AN OPENSITE PROGRAM
def seeReports(userDict, inputList):
    status = userDict.get("status", "guest")
    if meetsReqs(status,"moderator")>=0:
        try:
            allReports = os.listdir("Saved_Threads/staffChat")
            newHTML = "<ul>"
            for j in allReports:
                toPut = " ".join(j.split("_"))[:-4]
                #print "\t" + toPut
                toPut= '''
                <form method = get action = openSite.py>
                <input type = hidden name = isForum value = %s>
                <input type = hidden name = category value = staffChat>
                <input type = hidden name = userID value = %d>
                <input type = submit value = %s>
                <input type = hidden name = fromSite value = forumHome.html>
                </form>
                '''%('"%s"'%(toPut),userID,'"%s"'%(toPut))
                #print toPut
                newHTML =newHTML.replace("<!--End Thread Names-->", "<li>"+toPut+"</li>\n<!--End Thread Names--> ")
                #print newHTML
            newHTML = newHTML.replace("<!--End Thread Names-->", "</ul>\n<!--End Thread Names-->")
        except:
            print "An error occured while trying to access the file."
    else:
        print "Sorry, this action can only be performed by Mods+."
def makeReportThread(userDict, inputList):
    import createThread
    if len(inputList)<1:
        print "Not enough input for this function!"
        return
    if meetsReqs(userDict.get("status", "guest"), "admin")>=0:
        if "id" in userDict:
            createThread.main2(userDict["id"], inputList[0], "staffChat")
        else:
            print "Sorry, your account isn't recognized by the site."
    else:
        print "Sorry, this action can only be performed by Admins+."
def closeThread(userDict,inputList):
    if len(inputList)<3:
        print "Not enough input for this function!"
        return
    threadName=inputList[0]
    category=inputList[1]
    reason=inputList[2]
    status = userDict.get("status","")
    username=userDict.get("uname", "")
    #set firstline to "THREAD CLOSED: User <username> has closed the thread because <reason>"
    import createThread
    if meetsReqs(status, "admin")>=0:
        print createThread.addToTop(threadName, category, "THREAD CLOSED: User %s has closed the thread because %s"%(username, reason))
    else:
        print "Sorry, this action can only be performed by Admins+."
def makeTimeStamp():
    import datetime
    today= datetime.datetime.today()
    amOrpm = "AM"
    if (today.hour)/12>0:
        amOrpm ="PM"
    today = "<i>%02d/%d/%04d %d:%02d %s</i> "%(today.month,today.day,today.year,today.hour%12,today.minute, amOrpm)
    return today
def seeUserPosts(userDict,inputList):
    if len(inputList)<1:
        print "Not enough input for this function!"
        return
    username=inputList[0]
    status = userDict.get("status", "guest")
    if meetsReqs(status, "member")>=0:
        users = accountUtilities.masterDict("userInfo.txt")
        userID = -1
        for i in users.keys():
            if users[i].get("uname", "")==username:
                userID = users[i].get("id", -1)
        if userID<-1:
            print "The user could not be found."
            return
        if meetsReqs(status,users[i].get("status","guest"))<0:
            print "Sorry, you can only see posts by people of the same or lower rank."
            return
        allUserPosts = accountUtilities.parseUserInfo(userID)
        for k in allUserPosts.get("POST", []):
            print k + "<br>"
    else:
        print "Sorry, this action can only be performed by Members+." 
def sendMessage(userDict, inputList):
    import datetime
    if len(inputList)<2:
        print "Not enough input for this function!"
        return
    username = inputList[0]
    message = inputList[1]
    status = userDict.get("status","guest")
    if meetsReqs(status, "member")>=0:
        users = accountUtilities.masterDict("userInfo.txt")
        userID = -1
        for i in users.keys():
            if users[i].get("uname", "")==username:
                userID = users[i].get("id", -1)
        if userID<-1:
            print "The user could not be found."
            return
        today= datetime.datetime.today()
        amOrpm = "AM"
        if (today.hour)/12>0:
            amOrpm ="PM"
        today = "<i>%02d/%d/%04d %d:%02d %s</i> "%(today.month,today.day,today.year,today.hour%12,today.minute, amOrpm)
        if accountUtilities.addToUserInfo("\nPM","<b>%s</b> (%s): "%(userDict.get('uname',''), today) + message, userID):
            print "PM sent!"
        else:
            print "PM could not be sent."
    else:
        print "Sorry, this action can only be performed by Members+." 
def viewMessages(userDict, inputList):
    allInfo = accountUtilities.parseUserInfo(userDict.get("id", -1))
    #print allInfo
    if allInfo!={}:
        oldMessages = allInfo.get("PM-OLD",[])
        newMessages = allInfo.get("PM", [])
        #print oldMessages
        #print newMessages
        for i in range(len(newMessages)):
            print newMessages[i] + "<br>\n"
        for j in oldMessages:
            print "<font style = 'color:gray'>%s</font><br>\n"%(j)
        allInfo["PM-OLD"] = oldMessages+newMessages
        #print allInfo["PM-OLD"]
        allInfo["PM"] = []
        #print allInfo
        accountUtilities.writeDictUserFile(allInfo,userDict.get("id", -1))
main()
