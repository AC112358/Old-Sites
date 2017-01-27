def extractGameFile():
    s=""
    try:
        f = open("web_game_file.txt","rU")
        s = f.read()
        f.close()
    except:
        return s
    return s
def rewriteGameFile(s):
    try:
        f = open("web_game_file.txt","w")
        f.write(s)
        f.close()
    except:
        return False
    return True
def addToUserFile(username,password):
    s = extractUserFile()
    s+="\n%s,%s"%(username,password)
    rewriteUserFile(s)
def extractUserFile():
    s = ""
    try:
        f = open("uInfo.txt",'rU')
        s = f.read()
        f.close()
    except:
        return s
    return s
def rewriteUserFile(s):
    try:
        f = open("uInfo.txt","w")
        f.write(s)
        f.close()
    except:
        return False
    return True

gameHeadings = ["username", "gameName","level","score"]
userHeadings=["username", "password"]
def makeGameDict():
    gameInfo = {}
    games = [i.split(",") for i in extractGameFile().split("\n") if i!=""]
    for j in games:
        d={}
        for k in range(len(j)):
            if k==2:
                d[gameHeadings[k]] = int(j[k])
            elif k==3:
                d[gameHeadings[k]] = float(j[k])
            else:
                d[gameHeadings[k]] = j[k]
        if j[0] not in gameInfo:
            gameInfo[j[0]] = {j[1]:d}
        else:
            gameInfo[j[0]][j[1]] = d
    return gameInfo
def makeUserDict():
    userInfo={}
    users = [i.split(",") for i in extractUserFile().split("\n") if i!=""]
    for j in users:
        d={}
        for k in range(len(j)):
            d[userHeadings[k]] = j[k] #note that this means levels & scores are strings!
        userInfo[j[0]] = d
    return userInfo

def writeGameDict(d):
    total = ""
    for i in d.keys():
        for k in d[i].keys():
            line=""
            for j in gameHeadings:
                line+=str(d[i][k][j])+","
            line = line[:-1]
            total+=line+"\n"
    return rewriteGameFile(total[:-1])
def writeUserDict(d):
    total=""
    for i in d.keys():
        line=""
        for j in userHeadings:
            line+=str(d[i][j])+","
        line = line[:-1]
        total+=line+"\n"
    return rewriteUserFile(total[:-1])

