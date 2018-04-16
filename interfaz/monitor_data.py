from PyQt4.QtCore import QTime, QTimer


class monitor_data:
    t = [] # measure time in ms
    heartRate = [] # heartRate in BPM
    o2saturation = [] # O2 saturation in %
    systolic_art = [] # Systolic Blood Pressure in mmHg
    diasolic_art = [] # Diasolic Blood Pressure in mmHg
    mean_art = [] # Mean Arterial Pressures in en mmHg
        
    def update(
        self, t, heartRate, o2saturation, systolic_art, diasolic_art,
        mean_art):

        # Do not add values we already have 
        if t in self.t:
            return
        self.t.append(t)
        self.heartRate.append(heartRate)
        self.o2saturation.append(o2saturation)
        self.systolic_art.append(systolic_art)
        self.diasolic_art.append(diasolic_art)
        self.mean_art.append(mean_art)
                
    def empty(self):
        self.t[:] = []
        self.heartRate[:] = []
        self.o2saturation[:] = []
        self.systolic_art[:] = []
        self.diasolic_art[:] = []
        self.mean_art[:] = []
        
    # @staticmethod
    def read_csv_to_dict(self, csv_file):
        # return data from the csv as a dictionary
        with open(csv_file, 'r') as f:
            lines = [line.split(',') for line in f]
            for i in range(len(lines)):
                if len(lines[i]) + 1 == len(lines[i+1]):
                    # this condition is strange because actual lines have a
                    # ',' at the end, but the titles don't
                    titles = lines[i]
                    data = lines[i+1:]
                    break
            data_dict = {
                key: [row[i] for row in data]
                for i,key in enumerate(titles)
            }
            return data_dict

    def _parse_time(self, time_str):
        time_str, period = time_str.split(' ')
        hours, minutes, seconds = map(int, time_str.split(':'))
        if period == 'PM':
            hours += 12
        return QTime().msecsTo(QTime(hours, minutes, seconds))

    def load_csv(self, csv_file):
        data_dict = self.read_csv_to_dict(csv_file)
        t_str = data_dict['Time']
        t = [self._parse_time(t_entry) for t_entry in t_str]

        for i in range(len(t)):
            try:
                self.update(
                    t[i],
                    int(data_dict['Heart Rate(/min)'][i]),
                    int(data_dict['SpO2(%)'][i]),
                    int(data_dict['Systolic BP(mmHg)'][i]),
                    int(data_dict['Diastolic BP(mmHg)'][i]),
                    int(data_dict['Mean BP(mmHg)'][i])
                )
            except ValueError:
                pass

