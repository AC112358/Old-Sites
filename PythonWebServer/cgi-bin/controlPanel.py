def main(userID):
    html = ""
    error = "The control panel HTML couldn't be opened."
    try:
        f = open("control_panel.html", "rU")
        html = f.read()
        f.close()
        error = "User ID is invalid."
        html = html.replace("<!--userID-->", "<input type = hidden name = userID value = %d>\n<!--userID-->"%(userID))
        """newHTML = html.split("\n")
        for i in range(len(newHTML)):
            if newHTML[i].startswith("<!--PERMS"):
                perms = newHTML[i].split(" ")[-1]
                if perms in ["guest","member","moderator","admin", "owner"]:
                    users = accountUtilities.masterDict("userInfo.txt")
                    userStatus =users.get(userID, {}).get("status","guest")
                    if staffControls.meetsReqs(userStatus, perms)<0:
                        newHTML = html[:html.rfind("<form", 0, """ 
    except:
        html = "<html><body>%s</html></body>"%(error)
    return html


"""
def main2(userID):
    import staffControls,accountUtilities
    #THIS WILL RETURN ALL STUFF TO BE PRINTED, NOT CONTENT-TYPE THOUGH
    html = ""
    error = "The control panel HTML couldn't be opened."
    try:
        f = open("control_panel.html", "rU")
        html = f.read()
        f.close()
        #print html
        error = "User ID is invalid."
        html = html.replace("<!--userID-->", "<input type = hidden name = userID value = %d>\n<!--userID-->"%(userID))
        newHTML = html.split("<!--*BUTTON*-->")
        error = "Reason for error is unknown. This code shouldn't be problematic."
        perms = ""
        #print newHTML
        for i in range(len(newHTML)):
            if newHTML[i].startswith("<!--BUTTON"):
                error = "Error processing data to send."
                vals = []
                total = ""
                for j in newHTML[i]:
                    if j=="=" or j == " ":
                        vals.append(total)
                        total=""
                    else:
                        total+=j
                vals.append(total)
                #print vals
                if vals.find("value")<len(vals)-1:
                    value = vals[vals.find("value")+1:vals.find('"', vals.find("value")+2)]
                    if vals.find("perms")<len(vals)-1:
                        #perms= vals[vals.find("perms")+1:vals.find('"', vals.find("perms")+2)]
                        print perms
                        if perms in ["guest","member","moderator","admin", "owner"]:
                            users = accountUtilities.masterDict("userInfo.txt")
                            userStatus =users.get(userID, {}).get("status","guest")
                            if staffControls.meetsReqs(userStatus, perms)<0:
                                perms = " hidden"
                    newHTML[i]+="\n<input type = submit value = %s%s>"%(value,perms)
        html = "<!--*BUTTON*-->".join(newHTML)
    except:
        html = "<html><body>%s</html></body>"%(error)
    return html
"""
