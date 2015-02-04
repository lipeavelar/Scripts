import fbconsole
import atom.data
import gdata.data
import gdata.contacts.client
import gdata.contacts.data
import getpass
from urllib import urlretrieve
from datetime import datetime
import os

def getEmail():
	friends = fbconsole.fql("SELECT uid,name FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me())")
	cont = 0
	naoPegou = []
	for entry in feed.entry:
		if  entry.title.text:
			#print entry.title.text
			pegou = 1
			for amigo in friends:
				if entry.title.text == amigo["name"]:
					print "Mudando foto: "+str(amigo["uid"]) + " " + (amigo["name"].encode("utf-8")).decode("utf-8")
					profile_pic = "https://graph.facebook.com/"+str(amigo["uid"])+"/picture?type=large"
					try:
						urlretrieve(profile_pic, str(amigo["name"].encode("utf-8")).decode("utf-8")+".jpg")
					except:
						print "Erro ao tentar modificar a foto de " + (amigo["name"].encode("utf-8")).decode("utf-8")
						continue
					client.change_photo(str(amigo["name"].encode("utf-8")).decode("utf-8")+".jpg",entry,"image/jpeg")
					cont += 1
					os.remove(str(amigo["name"].encode("utf-8")).decode("utf-8")+".jpg")
					pegou = 0
					break
			if pegou == 1:
				naoPegou.append(entry.title.text)
	print "Foram pegos " + str(cont) + " contatos.\n"
	for nome in naoPegou:
		print nome

print datetime.now()
fbconsole.AUTH_SCOPE = ['publish_stream','read_stream','email']
fbconsole.authenticate()
usr = raw_input()
passwd = raw_input()
client = gdata.contacts.client.ContactsClient()
client.client_login(usr, passwd, "myscript")
qry = gdata.contacts.client.ContactsQuery(max_results=3000)
feed = client.get_contacts(query=qry)
getEmail()
print datetime.now()