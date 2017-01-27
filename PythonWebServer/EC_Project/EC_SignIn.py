#! /usr/bin/python
import cgi,cgitb
cgitb.enable()
def main():
    print "Content-type: text/html\n"
    form = cgi.FieldStorage()
    if "sign_in" in form:
        if "username" in form and "password" in form:
            signIn(form.getvalue('username'),form.getvalue('password'))
        else:
            updateHTML(True,"Username &/or password not entered!")
    if "sign_up" in form:
        if "username" in form and "password" in form:
            signUp(form.getvalue('username'),form.getvalue('password'))
        else:
            updateHTML(True,"Username &/or password not entered!")
def signIn(username,password):
    import EC_ProcessFile
    users = EC_ProcessFile.makeUserDict()
    for i in users:
        if users[i].get("username","")==username and users[i].get("password","")==password:
            redirectHome(username)
            return
    updateHTML(True,"Username &/or password incorrect.")
def signUp(username,password):
    import EC_ProcessFile
    users = EC_ProcessFile.makeUserDict()
    toReturn=""
    if "," in username or "," in password:
        updateHTML(False,"No commas allowed in username or password.")
        return
    if username.split()==[]:
        updateHTML(False,"Username cannot be made of only whitespace.")
        return
    for i in users:
        if users[i].get("username","").lower().split()==username.lower().split():
            updateHTML(False,"There's already a similar or identical username.")
            return
    EC_ProcessFile.addToUserFile(username,password)
    updateHTML(False,"Account created!")
def updateHTML(signIn,message):
    html=""
    try:
        f =open("signIn.html","rU")
        html=f.read()
        f.close()
        tag="<!--SIGN UP ERROR-->"
        if signIn:
            tag="<!--SIGN IN ERROR-->"
        message = '''<div class = error>
<text class=signIn>
%s
</text>
</div>'''%(message)
        html=html.replace(tag,tag+message)
    except:
        html= "<html><body>ERROR</body></html>"
    print html
def redirectHome(username):
    html=""
    try:
        f =open("signIn.html","rU")
        html=f.read()
        f.close()
        tag="<!--REDIRECT-->"
        html=html.replace(tag,tag+
                              ('<META http-equiv="refresh" '+
                              'content="0;URL=EC_HomePage.py?'+
                              'username=%s">'%(username)))
    except:
        html= "<html><body>ERROR</body></html>"
    print html


main()
