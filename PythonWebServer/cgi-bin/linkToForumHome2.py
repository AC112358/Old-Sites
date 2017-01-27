#! /usr/bin/python
import cgi, cgitb, siteUtilities, os
cgitb.enable()

HTML_HEADER = '''Content-type: text/html\n'''

def main():
    form = cgi.FieldStorage()
    print HTML_HEADER
    userID = -1
    if "userID" in form:
        userID = form.getvalue("userID")
        if type(userID)==type(1):
            userID = int(userID)
        else:
            userID = -1
    main2(userID)
def main2(userID):
    allThreadNames = os.listdir("Saved_Threads")
    newHTML = siteUtilities.getHTML("forumHome.html")
    #print newHTML
    for i in allThreadNames:
        newHTML = newHTML.replace("<!--End Thread Names-->", "<b>%s</b><br><ul>\n<!--End Thread Names-->"%(" ".join(i.split("_"))))
        for j in os.listdir("Saved_Threads/"+i):
            #print j
            toPut = " ".join(j.split("_"))[:-4]
            #print "\t" + toPut
            toPut= '''
            <form method = get action = openSite.py>
            <input type = hidden name = isForum value = %s>
            <input type = hidden name = category value = %s>
            <input type = hidden name = userID value = %d>
            <input type = submit value = %s>
	    <input type = hidden name = fromSite value = forumHome.html>
            </form>
            '''%('"%s"'%(toPut),i,userID,'"%s"'%(toPut))
            #print toPut
            newHTML =newHTML.replace("<!--End Thread Names-->", "<li>"+toPut+"</li>\n<!--End Thread Names--> ")
            #print newHTML
        newHTML = newHTML.replace("<!--End Thread Names-->", "</ul>\n<!--End Thread Names-->")
    newHTML=newHTML.replace("<!--End Thread Names-->", addThreadButton()+"\n<!--End Thread Names-->")
    print newHTML

def addThreadButton():
    allCategories = ""
    names = os.listdir("Saved_Threads")
    for j in range(len(names)):
        names[j] = '%s'%(" ".join(names[j].split("_")))
        if j!=0:
            allCategories+="<option>%s</option>\n"%(names[j])
        else:
            allCategories+="<option selected>%s</option>\n"%(names[j])
    inputControls ='''
<form method = post action = createThread.py>
<input type = text size = 20 value = "Thread Name">
<select name = category>
%s
</select>
<input type = submit value = "Add Thread">
</form>
'''%(allCategories)
    return inputControls





#PUBLIC STATIC VOID MAIN
main()











        
