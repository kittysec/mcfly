import uuid, re, random, os, subprocess, time, threading, sys, string
from colorama import init

###Colors###
init(autoreset=True)
white = '\x1B[37m';dgray = '\x1b[90m';DGRAY = '\x1b[100m';lred = '\x1b[91m';LRED = '\x1b[101m';lgreen = '\x1b[92m';LGREEN = '\x1b[102m';lyellow = '\x1b[93m';LYELLOW = '\x1b[103m';lblue = '\x1b[94m';LBLUE = '\x1b[104m';lmagenta = '\x1b[95m';LMAGENTA = '\x1b[105m';lcyan = '\x1b[96m';LCYAN = '\x1b[106m';lgray = '\x1b[97m';LGRAY = '\x1b[107m';BOLD = '\x1B[1m'

###Art###
print lyellow + '''
   ___           __         
  / _ )___ _____/ /__       
 / _  / _ `/ __/  '_/       
/____/\_,_/\__/_/\_\        
/_  __/__/_  __/ /  ___     
 / / / _ \/ / / _ \/ -_)    
/_/__\___/_/_/_//_/\__/     
  / __/_ __/ /___ _________ 
 / _// // / __/ // / __/ -_)
/_/  \_,_/\__/\_,_/_/  \__/ 

MCfly is an interactive program that spoofs 
MAC addresses in a given interval.
Author is not responsible to any damage caused
by this program

KittySec(C)                            
'''

###List of vendor MAC prefix
vendors = ['00:05:9A', '00:19:56', '00:02:B3', '00:00:C6', '00:11:11', '00:48:54'] 

def countdown(t):
	while t:	
	      	mins, secs = divmod(t, 60)
       		timeformat = '{:02d}:{:02d}'.format(mins, secs)
		sys.stdout.write(lmagenta + '\r' + '[info]' + white + ' Next spoof in: ' + str(timeformat).strip('\'\(\)') + ' seconds\r')
		sys.stdout.flush()
	       	time.sleep(1)
	        t -= 1
	       
def rand(size=2, chars=string.hexdigits):
	return str(''.join(random.choice(chars) for _ in range(size)))

def generateMAC():
	randomMAC = random.choice(vendors) + ':' + rand() + ':' + rand() + ':' + rand()
	return str(randomMAC).upper()

def spoofMAC(iface, interval):
	threading.Timer(interval, spoofMAC, [iface, interval]).start()
	try:
		#Parse ifconfig
		generatedMAC = generateMAC()
		cmd = 'ifconfig ' + str(iface) + ' hw ether ' + generatedMAC
		os.system(cmd)
		spoofedMAC = str(subprocess.check_output(['ifconfig'])).split('HWaddr')
		spoofedMAC = spoofedMAC[1].split(' ')
		spoofedMAC = spoofedMAC[1]
	
		#Check for successful spoofing
		if spoofedMAC.upper() == generatedMAC:
			print lgreen + '[+]' + ' Spoofed MAC address to ' + generatedMAC
			countdown(interval)
		else:
			print lred + '[-] There was an error'
	except Exception, e:
		print lred + '[-] Error ' + str(e)


originalMAC = str(':'.join(re.findall('..', '%012x' % uuid.getnode()))).upper()
print lmagenta + '[info] ' + white + 'Original MAC address is: ' + originalMAC

#List available interfaces
availIfaces = str(os.listdir('/sys/class/net/'))

#Take user input
iface = str(raw_input(lyellow + '[?] Choose interface: ' + availIfaces + '\n'))
interval = int(raw_input(lyellow + '[?] Each how many minutes would you like to spoof to a newer MAC address?\n'))
interval = interval * 60
spoofMAC(iface, interval)
