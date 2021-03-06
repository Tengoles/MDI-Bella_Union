import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from PyQt4.QtCore import QTime, QTimer
import numpy as np
from datetime import datetime
import time
import monitorData
import collections

csvPath = ""
timeScaleOptions = collections.OrderedDict([["5m",5*60*1000],
											["10m",10*60*1000],
											["15m",15*60*1000],
											["30m",30*60*1000],
											["1h",1*60*60*1000]
											])

#para poder etiquetar las graficas en el tiempo
class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super(TimeAxisItem,self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        # PySide's QTime() initialiser fails miserably and dismisses args/kwargs
        return [QTime().addMSecs(value).toString('hh:mm:ss') for value in values]


#inicializacion variables de interfaz grafica
app = QtGui.QApplication([])
win = QtGui.QMainWindow()
win.setWindowTitle('Operation Room #2')

#controles
pause_btn = QtGui.QPushButton()
pause_btn.setText("Pause")
time_lbl = QtGui.QLabel()
time_lbl.setText("Time scale: ")
time_lbl.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
cb = QtGui.QComboBox()
cb.addItems(timeScaleOptions.keys())
load_btn = QtGui.QPushButton()
load_btn.setText("Load CSV")

#graficas
pl1 = pg.PlotWidget(title = "Heart Rate (BPM)", axisItems={'bottom': TimeAxisItem(orientation='bottom')})
pl1.showGrid(x=True, y=True)
pl1.setMouseEnabled(y=False)
pl2 = pg.PlotWidget(title = "O2 Saturation (%)", axisItems={'bottom': TimeAxisItem(orientation='bottom')})
pl2.showGrid(x=True, y=True)
pl2.setMouseEnabled(y=False)
pl3 = pg.PlotWidget(title = "Blood Pressure (mmHg)", colspan = 2, axisItems={'bottom': TimeAxisItem(orientation='bottom')})
pl3.showGrid(x=True, y=True)
pl3.setMouseEnabled(y=False)
legend = pl3.addLegend()
pl3.plot(name="Systolic Arterial BP", pen = "m")
pl3.plot(name="Mean Aterial BP", pen = "r")
pl3.plot(name="Diasolic Arterial BP", pen = "g")

#grafica scrolleo
plScroll = pg.PlotWidget(title = "Time Selection", axisItems={'bottom': TimeAxisItem(orientation='bottom')})
plScroll.showGrid(x=True, y=True)
plScroll.setMouseEnabled(y=False)
region = pg.LinearRegionItem()
region.setZValue(99)
# Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this 
# item when doing auto-range calculations.
plScroll.addItem(region, ignoreBounds=True)

#formato de la ventana
layout = pg.LayoutWidget()
layout.addWidget(load_btn)
#layout.nextCol() #esto porque saque el boton de pausa
layout.nextCol()
layout.addWidget(time_lbl)
layout.addWidget(cb)
layout.nextRow()
layout.addWidget(pl1,colspan=2)
layout.addWidget(pl2,colspan=2)
layout.nextRow()
layout.addWidget(pl3, colspan=4)
layout.nextRow()
layout.addWidget(plScroll,colspan=4)
win.setCentralWidget(layout)
win.show()


#inicializacion buffers para las graficas
myData = monitorData.monitorData()
is_paused = True

#inicializar las graficas
def monitorDataInit(myData, csvPath):
	with open(csvPath, "r") as f:
		for line in f:
			try:
				resultados = map(int, line.split(','))
				t_ms = QTime().msecsTo(QTime(resultados[3], resultados[4], resultados[5]))
				myData.update(t_ms, resultados[6], resultados[7], resultados[8], resultados[9], resultados[10])
			except:	
				pass
				
#read line from csv
def readLineCSV(path, line):
	with open(path, "r") as f:
		last_line = f.readlines()[line]
		return map(int, last_line[:-1].split(','))
	
#update plot 1
def updatePlot1(myData):
	pl1.clear()
	pl1.plot(myData.t, myData.heartRate, pen="y")
	plScroll.plot(myData.t, myData.heartRate, pen="y")
	
#update plot 2
def updatePlot2(myData):
	pl2.clear()
	pl2.plot(myData.t, myData.o2saturation, pen="c")
	plScroll.plot(myData.t, myData.o2saturation, pen="c")
	
#update plot 3
def updatePlot3(myData):	
	pl3.clear()
	pl3.plot(myData.t, myData.systolic_art, pen="m")
	pl3.plot(myData.t, myData.diasolic_art, pen="g")
	pl3.plot(myData.t, myData.mean_art, pen="r")
	plScroll.plot(myData.t, myData.systolic_art, pen="m")
	plScroll.plot(myData.t, myData.diasolic_art, pen="g")
	plScroll.plot(myData.t, myData.mean_art, pen="r")

##update all plots
#def update(myData):
#	global is_paused
#	
#	if is_paused:
#		return
#	#leer csv	
#	resultados = readLineCSV("data.csv", -1) 
#	t_ms = QTime().msecsTo(QTime(resultados[3], resultados[4], resultados[5]))
#	
#	if t_ms != myData.t[-1]:
#		myData.update(t_ms, resultados[6], resultados[7], resultados[8], resultados[9], resultados[10])	
#		updatePlot1(myData)
#		updatePlot2(myData)
#		updatePlot3(myData)
	
#def pause():
#	global is_paused, pause_btn
#	is_paused = not is_paused
#	if is_paused:
#		pause_btn.setText("Resume")
#	else:
#		pause_btn.setText("Pause")

def updateTimeScale():
	maxX = region.getRegion()[1]
	minX = maxX - timeScaleOptions[str(cb.currentText())]
	region.setRegion([minX, maxX])
	
def updateRegion(window,viewRange):
    rgn = viewRange[0]
    region.setRegion(rgn)

def updatePlotFocus():
	minX, maxX = region.getRegion()
	pl1.setXRange(minX, maxX, padding=0)    
	pl2.setXRange(minX, maxX, padding=0)
	pl3.setXRange(minX, maxX, padding=0)

def getfile():
	global csvPath
	dlg = QtGui.QFileDialog()
	dlg.setFileMode(QtGui.QFileDialog.AnyFile)
	dlg.setFilter("CSV files (*.csv)")
	filenames = QtCore.QStringList()

	if dlg.exec_():
		filenames = dlg.selectedFiles()
		csvPath = str(filenames[0])
		
		myData.empty()
		monitorDataInit(myData,csvPath)
		updatePlot1(myData)
		updatePlot2(myData)
		updatePlot3(myData)
		region.setRegion([myData.t[-1]-timeScaleOptions[str(cb.currentText())], myData.t[-1]])

region.sigRegionChanged.connect(lambda: updatePlotFocus())


#timer = pg.QtCore.QTimer()
#timer.timeout.connect(lambda: update(myData))
#timer.start(500)
#pause_btn.clicked.connect(pause)
load_btn.clicked.connect(getfile)
cb.currentIndexChanged.connect(lambda: updateTimeScale())

pl1.sigRangeChanged.connect(updateRegion)
pl2.sigRangeChanged.connect(updateRegion)
pl3.sigRangeChanged.connect(updateRegion)



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
		
	
