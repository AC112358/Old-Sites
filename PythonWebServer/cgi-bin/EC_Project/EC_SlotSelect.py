#! /usr/bin/python
import cgi,cgitb
cgitb.enable()

def selectSlot(username,slotName): #return dictionary at the thing
    import EC_ProcessFile
    games = EC_ProcessFile.makeGameDict()
    if username not in games:
        games[username]={}
    if slotName in games[username]:
        return games[username][slotName]
    else:
        if slotName.split()==[]:
            return "No all-whitespace slot names allowed."
        for i in games[username].keys():
            if i.split()==slotName.split():
                return "There is already a slot with a very similar or identical name."
        games[username][slotName]={"username":username,"gameName":slotName,"level":0,"score":0.0}
        EC_ProcessFile.writeGameDict(games)
        return "Slot made!"
def main():
    print "Content-type: text/html\n"
    form = cgi.FieldStorage()
    slot = ""
    username=""
    proceed = True
    if "username" in form:
        username = form.getvalue("username")
    if "slot" in form: #note that this means people can't override old slots by making a new one with the same name
        slot = form.getvalue("slot")
    else:
        proceed = False
    vals=""
    mode = "MESSAGE"
    if proceed:
    	vals = selectSlot(username,slot)
    	if type(vals)==type({"hi":"bye"}):
           mode ="REDIRECT"
    updateHTML(mode,vals,username)
def updateHTML(mode,value,username):
    html=""
    try:
        f = open("slotPage.html","rU")
        html = f.read()
        f.close()
        import EC_ProcessFile
        games = EC_ProcessFile.makeGameDict()
        #print games[username]
        dropdown="<select name = slot>\n"
        for i in games.get(username,{}).keys():
            if "gameName" in games[username][i]:
                dropdown+='''<br><option>%s</option>\n'''%(games[username][i]["gameName"])
        dropdown+="</select>"
        html = html.replace("<!--SLOT SELECT-->","%s<!--SLOT SELECT-->"%(dropdown))
        html =html.replace("<!--INPUT USERNAME-->","<input type = hidden name = username value =%s><!--INPUT USERNAME-->"%(username))
        if mode.upper()=="REDIRECT":
            html=html.replace("<!--REDIRECT-->",
                              ('<!--REDIRECT--><META http-equiv="refresh" '+
                              'content="0;URL=EC_OpenSite.py?'+
                              'username=%s&gameName=%s&level=%d">')%(value["username"],value["gameName"],value["level"]))
        else:
            if value!="":
                value='''<div class = error>
                <text class=signIn>
                %s
                </text>
                </div>'''%(value)
            else:
                value = "<text class=signIn>%s</text>"%(value)
            html=html.replace("<!--MESSAGE-->","%s<!--MESSAGE-->"%(value))
    except:
         html= "<html><body>ERROR</body></html>"
    print html

main()
