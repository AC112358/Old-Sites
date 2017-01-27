#! /usrs/bin/python
import cgi, cgitb
cgitb.enable()

attackNames={"Water":0,"Earth":1,"Fire":2,"Air":3}
names = ["Korra", "Kyoshi", "Roku", "Aang"]
attacks = ["Water", "Earth", "Fire","Air"]
avatars = {}
def main():
    print "Content-type: text/html"
    form = cgi.FieldStorage()
    try:
        f = open("CharacterInfo.txt", "rU")
        s = f.read()
        f.close()
    except:
        s = ""
    avatars = setup(s)
    #print avatars
    html = getHTML()
    if "unlock" in form and "name" in form and "element" in form:
        avatars = unlockElement(form.getvalue("name"), form.getvalue("element"),avatars)
    if "attack" in form and "attacker" in form and "target" in form and "move" in form:
        outputs = attack(form.getvalue("attacker"), form.getvalue("target"), form.getvalue("move"),avatars)
        output = outputs[0]
        avatars=outputs[1]
        html = html.replace("<!--output-->", output+"<!--output-->")
        writeHTML(html)
    printHTML(html,avatars)
    writeAvatars(avatars)
def setup(s):
    allAvatars = [i.split(";") for i in s.split("\n") if i!=""]
    avatars = {}
    for j in range(len(allAvatars)):
        avatars[allAvatars[j][0]] = [k.split(",") for k in allAvatars[j]]
    return avatars

def attack(attacker,target, move,avatars):
    output=""
    if int(avatars[attacker][3][names.index(target)])>=2:
        output += "\n%s has already attacked %s twice! Attack unsuccessful."%(attacker.upper(), target.upper())
        return output
    avatars[target][1][0]=str(int(avatars[target][1][0])-20)
    avatars[attacker][3][names.index(target)]+=str(int(avatars[attacker][3][names.index(target)])+1)
    avatars[attacker][2][attackNames[move]]="False"
    output += "\n%s successfully attacked %s using %s!"%(attacker.upper(), target.upper(), move.upper())
    if int(avatars[attacker][3][names.index(target)])>=2:
        output += "\n%s cannot further attack %s."%(attacker.upper(), target.upper())
    print avatars
    return output,avatars
        
def printHTML(s,avatars):
    for i in names:
        s = s.replace("<!--Dropdown %s-->"%(i), makeDropdown(i,avatars))
        s = s.replace("<!--HP %s-->"%(i), avatars[i][1][0])
    print s


def getHTML():
    try:
        f = open("ChemGameSite.html", "rU")
        s = f.read()
        f.close()
    except:
        return ""
    return s
def writeHTML(newHTML):
    try:
        f = open("ChemGameSite.html", "w")
        f.write(newHTML)
        f.close()
    except:
        return False
    return True

def makeDropdown(name,avatars):
    dropdown = "<select>"
    for i in range(len(avatars[name][2])):
        if avatars[name][2][i]=="True":
            dropdown+="<option>%s Attack</option>"%(attacks[i])
    dropdown+="</select>"
    return dropdown
def unlockElement(name,element,avatars):
    avatars[name][2][attackNames[element]]="True"
    return avatars
    
def writeAvatars(avatars):
    toWrite = ""
    index1=0
    for i in names:
        if index1!=0:
            toWrite+="\n"
        for j in range(len(avatars[i])):
            if j!=0:
                toWrite+=";"
            toWrite+=",".join(avatars[i][j])
        index1+=1
    try:
        f = open("CharacterInfo.txt","w")
        f.write(toWrite)
        f.close()
    except:
        return False
    return True
            
            
main()
