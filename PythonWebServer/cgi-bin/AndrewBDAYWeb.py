#!/usr/bin/python
import cgi, cgitb
cgitb.enable()
form = cgi.FieldStorage()
HTML_HEADER = "Content-type: text/html\n\n"
Top_HTML = '''
<html><body>
'''
Bottom_HTML = '</html></body>'

def finishUp(display,total):
    if display:
        print total
    print "\nFUNCTION OUTPUT: "
def lvl0(takeIn, display):
    total ="\nCODE:\n"
    total+= ('''print "Hello %s!"'''%(takeIn))+"\n"
    print "Hello %s!"%(takeIn)
    finishUp(display, total)
def lvl1(takeIn, display):
    print "I learned very early the difference between knowing the name of %s and knowing %s."%(takeIn, takeIn)
    total ="\nCODE:\n"
    total+='''print "I learned very early the difference between knowing the name of %s and knowing %s."'''%(takeIn, takeIn)
    finishUp(display, total)
def readFile(filename):
    try:
        f = open(filename, "rU")
        s = f.read()
        f.close()
    except:
        print "ERROR: FILE %s NOT FOUND"%(filename)
        sys.exit(0)
        return False
    lines = s.split("\n")[1:]
    nameGames={}
    for i in range(len(lines)):
        temp = lines[i].split(",")
        nameGames[temp[0]]=[temp[1],temp[2]]
    return nameGames
def lvlSelect(nameGames):
    for i in nameGames.keys():
        print "Slot %s with level %s, score %s"%(i, nameGames[i][0], nameGames[i][1])
    while True:
        ans = raw_input("Enter the slot you want to play as or enter a new slot name (NO COMMAS): ")
        if "," not in ans:
            return ans
def run(currentLvl, slot_name, score, inputs, lvls):
    fName = "game_file.txt"
    nameGames= readFile(fName)
    slot_name = lvlSelect(nameGames)
    for i in range(currentLvl,len(lvls)):
        print "\n\nLEVEL %d"%(i)
        currentLvl=i
        bonus = 500
        print "\nOUTPUT:"
        print lvls[i](inputs[i][0], True)
        while True:
            takeIn= raw_input("\nEnter input. Enter nothing to guess the changed value. Enter 'quit' (no quotations) to quit: ")
            if takeIn =="":
                guess = raw_input("Guess the value in the original code that got changed: ")
                if guess==inputs[i][0]:
                    """guess = raw_input("Also state the line it's on (starting with line 1): ")
                    if guess == inputs[i][1]:"""
                    print "Nice job!"
                    bonus+=i*100
                    score+=bonus
                    print "You've gained %d points!"%(bonus)
                    print "Score: %d"%(score)
                    break
                    """else:
                        print "Sorry, that guess was incorrect."
                        if bonus>=25:
                            bonus-=25"""
                else:
                    print "Sorry, that guess was incorrect."
                    if bonus>=50:
                        bonus -= 50
            elif takeIn.lower()=="quit":
                return startSaving(fName, currentLvl, slot_name, score,nameGames)     
            else:
                print
                if bonus+i*100>=100:
                    bonus-=100
                print lvls[i](takeIn,False)
    print "Congratulations! You won the game!"
    return startSaving(fName, currentLvl, slot_name, score,nameGames)    
def startSaving(fName, currentLvl, slot_name,score,nameGames):
    endGame = raw_input("Would you like to save? If not, enter 'quit' (no quotations) to quit. ")
    if endGame=="quit":
        print "Bye!"
        return
    else:
        while True:
            slot =raw_input("Enter a new name to save game under a new slot (DO NOT name it with commas!). Enter nothing to save under the current slot %s: "%(slot_name))
            if "," in slot:
                print "I said no commas!"
            if slot=="":
                saveGame(fName,currentLvl, slot_name, score, nameGames)
                print "Game saved!"
                return
            else:
                if slot in nameGames:
                    override = raw_input("There is already a slot with that name. It has a level of %d and a score of %d. Do you want to override it? Enter 'yes' (no quotes) to override. "%(currentLvl, score))
                    if override.lower()=='yes':
                        slot_name = slot
                        saveGame(fName,currentLvl, slot_name, score,nameGames)
                        print "Game saved!"
                        return
                else:
                    slot_name = slot
                    saveGame(fName,currentLvl, slot_name, score,nameGames)
                    print "Game saved!"
                    return
            
def saveGame(filename, currentLvl, slot_name, score,nameGames):
    #import os
    try:
        f = open(filename, "rU")
        s = f.read()
        f.close()
        f = open(filename, "w")
        if slot_name not in nameGames: 
            f.write(s)
            f.write("\n%s,%d,%d"%(slot_name,currentLvl,score))
        else:
            f.write("NAME,LEVEL,SCORE")
            nameGames[slot_name] =[currentLvl,score]
            for i in nameGames.keys():
                f.write("\n%s,%d,%d"%(i,nameGames[i][0],nameGames[i][1]))
        f.close()
    except:
        print "ERROR: FILE %s NOT FOUND"%(filename)
        sys.exit(0)
        return False


inputs = [["world","1"], ["something","1"]]
lvls = [lvl0, lvl1]
slot_name = ""
currentLvl=0
score = 0
#print currentLvl
run(currentLvl, slot_name, score, inputs, lvls)
