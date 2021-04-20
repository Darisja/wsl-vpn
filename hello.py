import tkinter as tk
import re
import json
from urllib.request import urlopen
import requests
import requests, os, sys, tempfile, subprocess, base64, time
Height = 500
Width = 600

root = tk.Tk()
#api.openweathermap.org/data/2.5/forecast?q={city name}&appid={your api key}
#be54c7562705fefd72b5c3fa8f41836f
def format_response(data):
	
		try:
			IP=data['ip']
			org=data['org']
			city = data['city']
			country=data['country']
			region=data['region']

			final_str = ('IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0}'.format(org,region,country,city,IP))
		except:
			final_str = 'There was a problem retrieving that information'

		return final_str
	


def get_location():
	

	url = 'http://ipinfo.io/json'
	response = urlopen(url)
	data = json.load(response)

	IP=data['ip']
	org=data['org']
	city = data['city']
	country=data['country']
	region=data['region']

	#print ('Your IP detail\n ')
	#print ('IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0}'.format(org,region,country,city,IP))
	label1['text'] = format_response(data)




def check_connection():
	print("heloo")




def connect_vpn(entry1):
 
 x = entry1.get()
 y = str(x)
 if len(sys.argv) != 2:
	   print ('usage: ' + sys.argv[0] + ' ' +x)
	   
	
 

 if len(x) == 2:
	     i = 6 # short name for country
 elif len(x) > 2:
	     i = 5 # long name for country
 else:
	     print ('Country is too short!')
	     exit(1)

 try:
	     vpn_data = requests.get('http://www.vpngate.net/api/iphone/').text.replace('\r','')
	     servers = [line.split(',') for line in vpn_data.split('\n')]
	     labels = servers[1]
	     labels[0] = labels[0][1:]
	     servers = [s for s in servers[2:] if len(s) > 1]
 except:
	     print ('Cannot get VPN servers data')
	     exit(1)

 desired = [s for s in servers if x.lower() in s[i].lower()]
 found = len(desired)
 print ('Found ' + str(found) + ' servers for country ' + x)
 if found == 0:
	    exit(1)

 supported = [s for s in desired if len(s[-1]) > 0]
 print (str(len(supported)) + ' of these servers support OpenVPN')
	# We pick the best servers by score
 winner = sorted(supported, key=lambda s: float(s[2].replace(',','.')), reverse=True)[0]

 print( "\n== Best server ==")
 pairs = list(zip(labels, winner))[:-1]
 for (l, d) in pairs[:4]:
	     print( l + ': ' + d)

 print (pairs[4][0] + ': ' + str(float(pairs[4][1]) / 10**6) + ' MBps')
 print( "Country: " + pairs[5][1])

 print ("\nLaunching VPN...")
 _, path = tempfile.mkstemp()

 f = open(path, 'wb')
 
 f.write(base64.b64decode(winner[-1]))

 f.write(b'\nscript-security 2\nup /etc/openvpn/update-resolv-conf\ndown /etc/openvpn/update-resolv-conf')

 f.close()

 x = subprocess.Popen(['sudo' , 'openvpn' , '--config', path])

 try:
	 while True:
	     time.sleep(600)
	# termination with Ctrl+C
 except:
	 try:
	     x.kill()
	 except:
	     pass
	 while x.poll() != 0:
	     time.sleep(1)
	 print( '\nVPN terminated')


canvas = tk.Canvas(root, height=Height, width = Width)
canvas.pack()



frame = tk.Frame(root,bg = '#80c1ff',bd=7)
frame.place(relx = 0.5, rely =0.1,relwidth = 0.75,relheight = 0.1,anchor ='n')

entry1 = tk.Entry(frame)
entry1.place(relx=0.65,relwidth=0.3,relheight=1)

ch_button = tk.Button(frame, text="connect",font = 40,command = lambda: connect_vpn(entry1))
ch_button.place(relx=0.35,relwidth=0.3,relheight=1)



loc_button = tk.Button(frame, text="check location",font = 40,command = lambda: get_location())
loc_button.place(relx=0,relwidth=0.3,relheight=1)


lower_frame = tk.Frame(root,bg = '#80c1ff',bd=10)
lower_frame.place(relx = 0.5, rely =0.25,relwidth = 0.75,relheight = 0.6,anchor ='n')
label1 = tk.Label(lower_frame)
label1.place(relwidth=1,relheight=1)


root.mainloop()
