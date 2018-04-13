class monitorData:
	t = [] #tiempo de la medida en ms
	heartRate = [] #heartRate en BPM
	o2saturation = [] #o2 saturation en %
	systolic_art = [] #presion arterial systolica en mmHg
	diasolic_art = [] #presion arterial diasolica en mmHg
	mean_art = [] #presion arterial media en mmHg
	
	def update(self, t, heartRate, o2saturation, systolic_art, diasolic_art, mean_art):
		if len(self.t) > 0 and self.t[-1] == t:
			return
		self.t.append(t)
		self.heartRate.append(heartRate)
		self.o2saturation.append(o2saturation)
		self.systolic_art.append(systolic_art)
		self.diasolic_art.append(diasolic_art)
		self.mean_art.append(mean_art)
		
	def empty(self):
		self.t[:] = [] #tiempo de la medida en ms
		self.heartRate[:] = [] #heartRate en BPM
		self.o2saturation[:] = [] #o2 saturation en %
		self.systolic_art[:] = [] #presion arterial systolica en mmHg
		self.diasolic_art[:] = [] #presion arterial diasolica en mmHg
		self.mean_art[:] = [] #presion arterial media en mmHg
	
