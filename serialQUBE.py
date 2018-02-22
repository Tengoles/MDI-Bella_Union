import serial
import datetime

def word_in_string(word_list,a_string):
	return set(word_list).intersection(a_string.split())

def parseSPACE(x_string):
	largo=len(x_string)
	new_Str=''
	comaFlag=True
	for i in range(largo):
		if x_string[i]==' ':
			if comaFlag:
				new_Str=new_Str+';'   #pone una coma donde habria un espacio (para formato CSV supongo)
				comaFlag=False
		elif x_string[i]=='/':
			pass
		elif x_string[i]==':':
			new_Str=new_Str+';'
		elif x_string[i]=='I':
			pass
		elif x_string[i]=='?':
			pass
		else:
			comaFlag=True
			new_Str=new_Str+x_string[i]
	
	lastStr=new_Str.replace(".;","")
	#d= datetime.datetime.now()
       	#fechaStr = str(d.year) + ';' + str(d.month) + ';' + str(d.day) + ';'
	#lastStr = fechaStr  +  lastStr	
	#lastStr  = ';' +  str(d.day) + ';' +  lastStr #aux = "%s%s"%(fechaStr, lastStr) #.join([fechaStr, lastStr])
	#lastStr = ';' + str(d.month) + lastStr
	#lastStr = str(d.year) + lastStr
	#print lastStr
	#ultimoStr = lastStr.replace("@", fechaStr)
	return lastStr
			

word_list=['REGISTRADOR', 'ECG', 'NOMBRE', 'HORA', '********', '\n']

ser = serial.Serial(port = '/dev/ttymxc2', baudrate=9600) 
ser.flush()
ser.close()
ser.open()
while ser.isOpen():
	x = ser.readline()
	if word_in_string(word_list,x):
		pass
	else:
		print (x)
		recorte=parseSPACE(x)
		recorte=recorte[:-1]
		#print "estoy afuera"
		print recorte
		#d= datetime.datetime.now()
                #fechaStr = str(d.year) + ';' + str(d.month) + ';' + str(d.day) + ';'
		#auxStr = ''
		#for i in fechaStr:
		#	auxStr = auxStr + i
		#for i  in recorte:
		#	auxStr = auxStr +i
		#print "Holu"
		#print len(recorte)
		#print len(fechaStr)
		#print auxStr
		#print len(auxStr)
		if len(recorte)>2:
			print recorte[0]
			if recorte[1]=='*':
				with open('/home/udooer/Desktop/MDI-Bella_Union/logs/tempAlarm.csv','a') as alarmCSV:
					alarmCSV.write(recorte)
			else:
				#d= datetime.datetime.now()
       				#fechaStr = str(d.year) + ';' + str(d.month) + ';' + str(d.day) + ';'
        			#lastStr = fechaStr  +  lastStr 
				#print fechaStr + recorte
				with open('/home/udooer/Desktop/MDI-Bella_Union/logs/temporal.csv','a') as CSV:
					CSV.write(recorte)

ser.close()
