def checkInfo(uName, pW, filename):
    idNum = -1
    allInfo = getAccounts(filename)
    allInfo = [i.split(",") for i in allInfo.split("\n") if i!=""]
    for i in allInfo:
        if "".join(uName.split()).lower()=="".join(i[1].split()).lower() and "".join(pW.split()).lower()=="".join(i[2].split()).lower():
            idNum = int(i[0])
    return idNum
def getAccounts(filename):
    try:
        f = open(filename, "rU")
        s = f.read()
        f.close()
    except:
       return ""
    return s
allHeadings = ["id", "uname","pw", "status"]
def masterDict(filename):
    allInfo = getAccounts(filename)
    allInfo = [i.split(",") for i in allInfo.split("\n") if i!=""]
    d={}
    for i in allInfo:
        e={}
        for j in range(len(i)):
            if j==0 and i[j].isdigit():
                e[allHeadings[j]] = int(i[j])
            if j!=0:
                e[allHeadings[j]] = i[j]
        if i[0].isdigit():
            d[int(i[0])] = e
    return d
def writeDict(users,filename):
    fullText = ""
    for i in users.keys():
        fullText+=str(users[i]["id"])
        for j in allHeadings[1:]:
            fullText+="," + str(users[i].get(j,""))
        fullText+="\n"
    fullText = fullText[:-1]
    try:
        f = open(filename, "w")
        f.write(fullText)
        f.close()
    except:
        return False
    return True
def writeDictUserFile(userInfo,userID):
    import os
    fullText = ""
    #print userInfo
    for i in userInfo.keys():
        #print i + ": " + str(userInfo[i])
        if userInfo[i]!=None:
            for j in userInfo[i]:
                if j !="":
                    fullText+="\n" + i + "," + str(j)
            fullText+="\n"
    fullText = fullText[:-1]
    #print fullText
    try:
        fName = "Users/user_history_%d.txt"%(userID)
        if os.path.isfile(fName):
            f = open(fName, "w")
            f.write(fullText)
            f.close()
    except:
        return False
    return True
def makeAccount(uName, pW, filename): #False if username exists or file writing error
    allInfo = getAccounts(filename)
    allInfo = [i.split(",") for i in allInfo.split("\n") if i!=""]
    #print allInfo
    newLine = ""
    #test if exists
    #if not make new
    lowestID = 0
    if "," in uName:
        return 3
    for i in allInfo:
        if "".join(uName.split()).lower()=="".join(i[1].split()).lower():
            return 1
        lowestID+=1
    return writeLine(uName, pW, lowestID, filename)
def writeLine(uName, pW, userID, filename):
    try:
        f = open(filename, "rU")
        s = f.read()
        f.close()
        f = open(filename, "w")
        f.write(s)
        f.write("%d,%s,%s,member"%(userID, uName, pW))
        f.close()
        return 0
    except:
        return 2
def updateUserFile(userID, text):
    try:
        import os.path, subprocess
        fName = "Users/user_history_%d.txt"%(userID)
        s=""
        if os.path.isfile(fName):
            f = open(fName, "rU")
            s = f.read()
            f.close()
        f = open(fName, "w")
        f.close()
        subprocess.call(["chmod", "g+w", fName])
        subprocess.call(["chmod", "o+w", fName])
        f = open(fName, "w")
        f.write(s)
        f.write(text)
        f.close()
        return True
    except:
        return False
def makeUserFile(userID):
    return updateUserFile(userID, "")
def addToUserInfo(infoType, post, userID):
    toAdd = infoType + "," + post
    return updateUserFile(userID,toAdd)
def getUserInfo(userID):
    import os.path
    try:
       # print os.getcwd()
        #print os.path.exists("Users")
        fName = "Users/user_history_%d.txt"%(userID)
        s=""
        if os.path.isfile(fName):
            f = open(fName, "rU")
            s = f.read()
            f.close()
    except:
        return ""
    return s
def parseUserInfo(userID):
    userInfo = getUserInfo(userID)
    #print userInfo
    if "," not in userInfo:
        return {}
    allTypes = {}
    for i in userInfo.split("\n"):
        temp = [i[:i.find(",")], i[i.find(",")+1:]]
        if temp[0] in allTypes:
            allTypes[temp[0]].append(temp[1])
        else:
            allTypes[temp[0]] =[temp[1]]
    return allTypes
    
    
