import os
def makeThread(threadName, category):
    try:
        threadName = "_".join(threadName.split(" "))
        category = "_".join(category.split(" "))
        path = "Saved_Threads/%s/"%(category)
        if not os.path.isdir(path):   
            try:
                os.makedirs(path)
            except OSError:
                return False
        newFile = "%s.txt"%(threadName) 
        f = open(path+newFile, "w+")
        #print "got up to jere"
        f.close()
        return True
    except:
        return False
    return False
def addCategory(category):
    try:
        category = "_".join(category.split(" "))
        path = "Saved_Threads/%s/"%(category)
        allCategories = os.listdir("Saved_Threads/")
        for i in allCategories:
            if processString(i)==processString(category):
                return 2
        if not os.path.isdir(path):   
            try:
                os.makedirs(path)
                return 0
            except OSError:
                return 3
        else:
            return 2
    except:
        return 1
    return 1
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

def post(fullPost, threadName, category):
    threadName = "_".join(threadName.split(" "))
    category = "_".join(category.split(" "))
    path = "Saved_Threads/%s/"%(category)
    newFile = "%s.txt"%(threadName)
    try:
        proceed = True
        if not os.path.exists(path+newFile):   
            proceed =makeThread(threadName, category)
        if proceed:
            return addToThread(threadName, category, fullPost)
        return True
    except:
        return False
    return False
def getThreadContents(threadName, category):
    threadName = "_".join(threadName.split(" "))
    category = "_".join(category.split(" "))
    path = "Saved_Threads/%s/"%(category)
    newFile = "%s.txt"%(threadName)
    if os.path.exists(path+newFile):
        try:
            f = open(path+newFile, "rU")
            s = f.read()
            f.close()
            return s
        except:
            return ""
    else:
        return ""
def addToThread(threadName, category, newPost):
    import os, stat, sys, subprocess
    threadName = "_".join(threadName.split(" "))
    category = "_".join(category.split(" "))
    path = "Saved_Threads/%s/"%(category)
    newFile = "%s.txt"%(threadName)
    if os.path.exists(path+newFile):
        try:
            f = open(path+newFile, "rU")
            s = f.read()
            f.close()
            #print "hi first time"
            #os.chmod(path+newFile,stat.S_IWOTH)
            #os.chmod(path+newFile,stat.S_IWGRP)
            #subprocess.call(["chmod", "+w", path+newFile], shell=True)
            #print "\nhi again"
            f = open(path+newFile,"w")
            #print "ok the thing was opened"
            f.write(s)
            f.write(newPost)
            f.close()
            return True
        except:
            return False
    else:
        return False

def threadHTML(threadName, category, userID):
    #HTML_HEADER = "Content-type: text/html\n"
    s="<h1>%s</h1>"%(" ".join(threadName.split("_")))
    s += getThreadContents(threadName, category)
    try:
        f = open("forumLower.txt", "rU")
        s1=f.read()
        f.close()
        f = open("forumUpper.txt", "rU")
        s2 = f.read()
        f.close()
        if userID<0:
            return s1 + s + s2
        else:
            s+='''
            <br><b>Post here:</b><br>
            <form method = "get" action = "openSite.py">
            <textarea rows = 20 name="userPost" cols = 50 style = "resize:none"></textarea>
            <input type=hidden name=isForum value=%s>
            <input type=hidden name = category value=%s>
        <input type = submit value = Post>
            </form>
            '''%(threadName, category)
        return s1+s+s2
    except:
        return ""
        
statusColor = {"guest":"gray", "member":"blue", "moderator":"purple", "admin":"red", "owner":"#ff33cc"}
def makePost(username, status, text):
    status = status.lower()
    newPost = '''\n<b><font style = color:"%s">'''%(statusColor.get(status, "black")) + username.upper() + '''</b></font>: ''' + text
    return newPost
