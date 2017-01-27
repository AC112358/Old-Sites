def insertPost3(html, keyWord, keyEnd, insert):
    startI, startJ = -1,-1
    endI, endJ = -1,-1
    for i in range(len(html)):
        for j in range(i, len(html)):
            if "".join(html[i:j].split(" ")) == "".join(keyWord.split(" ")):
                startI, startJ = i,j
            if endI<0 and startI>0 and "".join(html[i:j].split(" ")) == "".join(keyEnd.split(" ")):
                endI,endJ = i,j
    html = html[:endI] + insert + html[endI:]
    #print html
    return html
def insertPost4(html, keyWord, keyEnd, insert):
    startI = -1
    endI = -1
    index = 0
    i = 0
    while i < len(html):
        j=0
        while j < len(html):
            if "".join(html[i:j].split(" ")) == "".join(keyWord.split(" ")):
                startI = i
            if endI<0 and startI>0 and "".join(html[i:j].split(" ")) == "".join(keyEnd.split(" ")):
                endI = i
                html = html[:endI] + insert + html[endI:]
                i = endI
                endI = -1
                startI = -1
            j+=1
        i+=1
    return html
def testInsert4(filename, userID):
    html = getHTML(filename)
    toReturn = insertPost4(html, "<form", "</form>","<input type = hidden name = userID value = %d>"%(userID))
    print toReturn
def modifyHTML(html, userID):
    toReturn = insertPost4(html, "<form", "</form>","<input type = hidden name = userID value = %d>"%(userID))
    #print toReturn
    return toReturn #THIS WILL ONLY MODIFY 1 OF THE FORMS!
def getHTML(filename):
    try:
        f = open(filename,"rU")
        s  = f.read()
        f.close()
        return s
    except:
        return ""
def getTagContents(html, keyWord, keyEnd):
    new_html = ""
    startI, startJ = -1,-1
    endI, endJ = -1,-1
    for i in range(len(html)):
        for j in range(i, len(html)):
            if "".join(html[i:j].split(" ")) == "".join(keyWord.split(" ")):
                startI, startJ = i,j
            if endI<0 and startI>0 and "".join(html[i:j].split(" ")) == "".join(keyEnd.split(" ")):
                endI,endJ = i,j
    #print html[startI:endJ]
    return html[startI:endJ]
def getVariableVal(html, keyWord, keyEnd, varName):
    tag = getTagContents(html, keyWord, keyEnd)
    tag = tag[:-len(keyEnd)]
    split_html=[]
    temp = ""
    for i in tag:
        if i==" " or i =="=":
            if temp!="":
                split_html.append(temp)
                temp = ""
        else:
            temp+=i
    split_html.append(temp)
    #print split_html
    if varName in split_html and (split_html.index(varName)<len(split_html)-1):
        return split_html[split_html.index(varName)+1]
    return ""
def getUserID(html):
    val = getVariableVal(html, "<input type = hidden name = userID", ">", "value")
    if val.isdigit():
        return int(val)
    return -1
def getIDFromFile(filename):
    new_html = getHTML(filename)
    return getUserID(new_html)
def modifyHTMLFile(filename, userID):
    new_html = getHTML(filename)
    s = modifyHTML(new_html, userID)
    return writeHTML(s, filename)
def writeHTML(s, filename):
    try:
        f = open(filename, "w")
        f.write(s)
        f.close()
    except:
        return False
    return True
def changeNewFromOld(old, new):
    userID = getIDFromFile(old)
    return modifyHTMLFile(new, userID)
