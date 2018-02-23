import serial
import datetime

def word_in_string(word_list,a_string):
	return set(word_list).intersection(a_string.split())

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def parseSPACE(x_string):
	aux = x_string[1:-3].split('   ')
	aux = [x for x in aux if is_number(x)]
	return ';'.join(aux)
	#largo=len(x_string)
	#new_Str=''
	#comaFlag=True
	#for i in range(largo):
		#if x_string[i]==' ':
			#if comaFlag:
				#new_Str=new_Str+';'   #pone una coma donde habria un espacio (para formato CSV supongo)
				#comaFlag=False
		#elif x_string[i]=='/':
			#pass
		#elif x_string[i]==':':
			#new_Str=new_Str+';'
		#elif x_string[i]=='I':
			#pass
		#elif x_string[i]=='\r':
			#pass
		#elif x_string[i]=='?':
			#pass
		#else:
			#comaFlag=True
			#new_Str=new_Str+x_string[i]
	
	#lastStr=new_Str.replace(".;","")
	
	#return lastStr
			

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
		
		print recorte
		
		if len(recorte)>2:
			print recorte[0]
			if recorte[1]=='*':
				with open('/home/udooer/Desktop/MDI-Bella_Union/logs/tempAlarm.csv','a') as alarmCSV:
					alarmCSV.write(recorte)
			else:
				with open('/home/udooer/Desktop/MDI-Bella_Union/logs/temporal.csv','a') as CSV:
					CSV.write(recorte)

ser.close()
