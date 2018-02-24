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

#agrega la fecha al principio de un string a ser almacenado
#tiene en cuenta si es una alarma
def insert_date(s):
	if s[0] == '*':
		i = 2
	else:
		i = 0
	date_str = datetime.datetime.now().strftime('%Y;%m;%d;%H;%M;%S;')
	return s[0:i] + date_str + s[i:]
	
#le entra un string recibido del equipo, se queda solo con los numeros
#y con el asterisco al principio (por si es una alarma)
#devuelve un string separado por ';'
def parseSPACE(x_string):
	x_string = x_string.replace('*', ' * ')
	aux = x_string.split(' ')
	aux = [x for x in aux if is_number(x) or x == '*']
	return ';'.join(aux)

word_list=['REGISTRADOR', 'ECG', 'NOMBRE', 'HORA', '********', '\n']
logs_path = '/home/udooer/Desktop/MDI-Bella_Union/logs/'

if __name__ == "__main__":
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
			recorte = insert_date(recorte)
			#recorte=recorte[:-1]
			print recorte
			
			if len(recorte)>2: #por que esta este filtro?
				#print recorte[0]
				if recorte[0]=='*':
					with open(logs_path + 'tempAlarm.csv','a') as alarmCSV:
						alarmCSV.write(recorte + '\n')
				else:
					with open(logs_path + 'temporal.csv','a') as CSV:
						CSV.write(recorte + '\n')

	ser.close()
