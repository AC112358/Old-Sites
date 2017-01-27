#! /usr/bin/python
import cgi, cgitb
cgitb.enable()
def intConvert(takeIn):
    try:
        int(takeIn)
        return True
    except:
        return False
def floatConvert(takeIn):
    try:
        float(takeIn)
        return True
    except:
        return False
from cStringIO import StringIO
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout
def listConvert(value,convert):
    try:
        x=list(value)
        if convert:
            return "\n".join(x)
        return x
    except:
        return value
def mainHelper(takeIn, display, function):
    toReturn=""
    tot = function(takeIn, display)
    if display:
        toReturn+= '\n<b style="font-size:20px">CODE: </b><br><div class=code><pre>'+str(tot)+'</pre></div>'
        toReturn+='<br><b style="font-size:20px">FUNCTION OUTPUT: </b>'
    else:
        toReturn+= '<br>>>>FUNCTION OUTPUT: '
    try:
        with Capturing() as output:
            exec(tot)
        output = listConvert(output,True)
        toReturn+="<pre>"+str(output)+"</pre>"
    except:
        import sys
        e = sys.exc_info()
        toReturn+="ERROR: " + str(e)
    return toReturn
def lvl1(takeIn,display):
    try:
        total = 'print "I learned very early the difference between knowing the name of %s and knowing %s."'%(takeIn, takeIn)
    except:
        total="print 'ERROR! Wrong input type.'"
    return total
def lvl2(takeIn,display):
    try:
        takeIn=int(takeIn)
        total= 'print "%d Easy Pieces"'%(takeIn)
    except:
        total="print 'ERROR! Wrong input type.'"
    return total
def lvl3(takeIn,display):
    error = ""
    total=""
    try:
        error = "Wrong input type."
        takeIn=int(takeIn)
        error = "Index out of bounds."
        total='''
Elements=["Bill Evans","Mark Egan", "Dan Gottlieb","Clifford Carter"]
print Elements[%d]
    '''%(takeIn)
    except:
        total="print 'ERROR! %s'"%(error)
    return total
def lvl5(takeIn, display):
    error=""
    try:
        error="Wrong input type."
        x = int(takeIn)
        error="List index out of range."
        total ='''
stem = ["Science", "Technology", "Engineering", "Math"]
for i in range(0,%d):
    print stem[i]
        '''%(x)
    except:
        total="print 'ERROR! %s'"%(error)
    return total
def tutorial(takeIn,display):
    if display:
        total='''
print "Welcome to the Python Input Game Tutorial!"
print "The Python Input Game is designed to teach you Python."
print "You are given some code and have to decide which value is a variable that you, the user, can alter."
print "You will only get the function code with the unchanged value to look at and see the output of."
print "You can try to find the changed value by inputting values into the function. These values will replace the current value of the user-controlled variable."
print "Then, the function output will be printed on the console."
print "Don't worry if the output says 'wrong output type' or is an error. This means your input caused the function to have an error."
print "You can also guess which value got changed."
print "Both inputting values & guessing take away some of the points you could get for a level."
print "However, you will always earn points for completing a level."
print "----------------------------"
print "Now let's try an example. Here is the phrase that gets changed: "
print "HELLO %s!"
print "So some value in 'HELLO world!' is up for you to control."
print "Try inputting values. You can do this by typing into the text box under 'INPUT:' and pressing 'Enter Input'."
print "Once you think you have an answer, enter the value you think you changed in the phrase 'HELLO world!'"
print "If you get it right, the console will tell you."
print "Good luck!"
    '''%(takeIn)
    else:
        total='''print "HELLO %s!"'''%(str(takeIn))
    return total
def gameInputs1():
    #return ["world", "something",4]
    return ["world","something",6,0,4]
def allLevels1():
    return [tutorial,lvl1,lvl2,lvl3,lvl5]
def mainGame(username, gameName,level,userInput,score,message):
    allLevels = allLevels1()
    gameInputs = gameInputs1()
    toPrint=""
    if level < len(allLevels):
        toPrint+=mainHelper(userInput,False,allLevels[level])
        if score>(level+1)*25:
            score-=10 #GUESSING PENALTY
    toPrint="<text style=color:#4CE8DD class=code>"+toPrint+"</text>"
    toPrint+="\n<br>"+message[len("\n<br><text style=color:#4CE8DD class=code>")+1:-len("</text>")]
    updateHTML(username, gameName,level,score,toPrint)
def guessVal(username,gameName,level,guess,score,message):
    toPrint=""
    gameInputs = gameInputs1()
    if level < len(gameInputs):
        if str(guess)==str(gameInputs[level]):
            toPrint+=">>>The guess was correct!"
            if level!=0:
                level+=1
            else:
                toPrint+="\n<br>>>>Now you've completed the Tutorial round! Go back Home to get started playing."
            if level>=len(gameInputs):
                toPrint+="\n<br>>>>Congratulations! You won the game!"
            import EC_ProcessFile
            games = EC_ProcessFile.makeGameDict()
            if username in games and gameName in games[username]:
                games[username][gameName]["score"]=games[username][gameName]["score"]+score
                EC_ProcessFile.writeGameDict(games)
        else:
            if score>(level+1)*25:
                score-=25 #GUESSING PENALTY
            toPrint+=">>>Sorry, that guess was incorrect."
    toPrint="<text style=color:#4CE8DD class=code>"+toPrint+"</text>"
    toPrint+="\n<br>"+message[len("\n<br><text style=color:#4CE8DD class=code>")+1:-len("</text>")]
    updateHTML(username, gameName,level,score,toPrint)
def updateHTML(username,gameName,level,score,message):
    html=""
    try:
        f = open("levelPage.html","rU")
        html = f.read()
        f.close()
        import EC_ProcessFile
        html = html.replace("<!--GAMENAME-->","<!--GAMENAME-->%s"%(gameName))
        html = html.replace("<!--LEVEL-->","<!--LEVEL-->%d"%(level))
        html = html.replace("<!--SCORE-->","<!--SCORE-->%.1f"%(float(score)))
        html = html.replace("<!--MESSAGE-->","%s<!--MESSAGE-->"%(message))
        html = html.replace("<!--USERNAME-->","<!--USERNAME-->%s"%(username))
        html = html.replace("<!--INPUT GAMENAME-->",'<!--INPUT GAMENAME--><input type=hidden name=gameName value="%s">'%(gameName))
        html = html.replace("<!--INPUT LEVEL-->","<!--INPUT LEVEL--><input type =hidden name = level value = %d>"%(level))
        html = html.replace("<!--INPUT SCORE-->",'<!--INPUT SCORE--><input type =hidden name = score value = %.1f>'%(float(score)))
        html = html.replace("<!--INPUT USERNAME-->",'<!--INPUT USERNAME--><input type=hidden name=username value="%s">'%(username))
        if level<len(gameInputs1()) and level<len(allLevels1()):
            html = html.replace("<!--FUNCTION CODE-->","%s<!--FUNCTION CODE-->"%(str(mainHelper(gameInputs1()[level], True,allLevels1()[level]))))
        html = html.replace("<!--INPUT MESSAGE-->",('<input type = hidden name = message value = "%s">'%(message)))#+html[html.find("<!--START MESSAGE-->")+len("<!--START MESSAGE-->"):html.find("<!--MESSAGE-->")])
                                                    #+ "<!--INPUT MESSAGE-->"))
        html = html.replace("<!--TOTAL SCORE-->","<!--TOTAL SCORE-->%.1f"%(float(EC_ProcessFile.makeGameDict().get(username,
                                                                                                                   {}).get(gameName,{}).get("score",0))))
        
    except:
        print ""
    print html
        
def main():
    print "Content-type: text/html\n"
    form = cgi.FieldStorage()
    level = 1
    username = "Guest"
    gameName = ""
    proceed = True
    score=0
    toPrint=""
    if "username" in form:
        username = form.getvalue("username")
    if "message" in form:
        toPrint+=form.getvalue("message")+"\n<br>"
    if "gameName" in form:
        gameName = form.getvalue("gameName")
    else:
        import datetime
        today = datetime.date.today()
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        gameName = "%s %d, %d" %(months[today.month-1],today.day,today.year)
    if "level" in form and form.getvalue("level").isdigit():
        level = int(form.getvalue("level"))
        if "score" in form and floatConvert(form.getvalue("score")):
            score = float(form.getvalue("score"))
        else:
            score = (level+1)*100
        if "userInput" in form:
            proceed = False
            userInput=form.getvalue("userInput")
            mainGame(username,gameName,level,userInput,score,toPrint)
        elif "guessAns" in form:
            proceed = False
            guess = form.getvalue("guessAns")
            guessVal(username,gameName,level,guess,score,toPrint)
    if proceed:
        updateHTML(username, gameName,level,score,toPrint)
main()
