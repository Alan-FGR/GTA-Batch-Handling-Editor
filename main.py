'''
Created on 
@author: Alan
'''

scrwidss = """
*{
border: none;
background: #eee;
font: normal 10px sans-serif;
}
 
QSpinBox::up-button, QDoubleSpinBox::up-button, QSpinBox::down-button, QDoubleSpinBox::down-button {
    border: 1px solid #ccc;
    height: 7px;
    width: 7px;
}

QPushButton {
    border: 1px solid #ccc;
}

QSpinBox::down-button, QDoubleSpinBox::down-button {
    border-top: none;
}

QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {
    image: url(./plus.png);
    width: 7px;
    height: 7px;
}

QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {
    image: url(./minus.png);
    width: 7px;
    height: 7px;
}

QToolTip {
    border: 1px solid #666;
    border-radius: 4px;
    color: #666;
    font-size: 12px;
}

"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class lineData():
    def __init__(self, line, lo, widslist):
        
#         forbiddentags = ["^", ";", "$", "#", "%", "!"]
#         boats = ["TUG","TROPIC","SQUALO","REEFER","PREDATOR","MARQUIS","JETMAX","DINGHY"]
#         helis = ["TOURMAV","POLMAV","MAVERICK","ANNHIL"]
#         other = ["FIGHTER","DODO","ANDROM","SUBWAY","CABLECAR",""]
        
        self.rawline = line
        ldata = None
        editorwidget = None
        
        global scrrow
        
        if line.split()[0][0] not in forbtags and line.split()[0] not in specialvehicles:
            ldata = line.split()
            
            cstl = "*{background:#def} *:hover {background: #efe}"
            if scrrow%2 == 0:
                cstl = "*{background:#cdf} *:hover {background: #dfd}"
            
            editorwidget = vEdLine(ldata, cstl)
            
            if scrrow%2 == 0:
                editorwidget.setStyleSheet("*{background:#eee} *:hover {background: #dfd}")
            else:
                editorwidget.setStyleSheet("*{background:#fff} *:hover {background: #efe}")
                
            scrrow+=1
            lo.addWidget(editorwidget)
            widslist.append(editorwidget)
            
        self.ldata = ldata
        self.editorw = editorwidget
            
        
    def getLine(self):
        if self.ldata is None:
            return self.rawline
        else:
            return self.editorw.getLine()+"\n"
        

# class NDSpinBox(QDoubleSpinBox):
#     def __init__(self):
#         QDoubleSpinBox.__init__(self)
#         
#     def focusInEvent(self, event):
#         print "focuses"

class itemHeader(QWidget):
    def __init__(self, text, tooltip, width, column, multfunc, sumfunc, setfunc, highlightcol):
        QWidget.__init__(self)
        
        self.column = column
        
        self.setFixedSize(width, 30)
#         self.setStyleSheet("border:1px solid blue; font: 10px")
        
        idlabel = QPushButton(text, self)
        idlabel.setStyleSheet("border:none; text-align:left")
        idlabel.setToolTip(tooltip)
        idlabel.setGeometry(0,0,width,16)
        idlabel.col = column
        idlabel.clicked.connect(highlightcol)
        
        multbut = self.createBut("x", "Multiply All Values in Column "+text, 0, 16, width/3, 16, multfunc)
        sumbut = self.createBut("+", "Add a Number to All Values in Column "+text, width/3, 16, width/3, 16, sumfunc)
        settbut = self.createBut("s", "Set All Values in Column "+text, width/1.58, 16, width/3, 16, setfunc)
        
        multbut.setGeometry(0,16,width/3,14)
        
        
    def createBut(self, btext, tooltip, x, y, width, height, func):
        b = QPushButton(btext, self)
        b.setToolTip(tooltip)
        b.setGeometry(x,y,width,height)
        b.clicked.connect(func)
        b.col = self.column
        return b
        

class hHLine(QWidget):
    def __init__(self, widslist):
        QWidget.__init__(self)
        
        hlo = QHBoxLayout(self)
        hlo.setContentsMargins(0, 0, 0, 0)
        hlo.setSpacing(0)
        
        namew = QLabel("EDIT ALL:")
        self.widslist = widslist
        
        self.setStyleSheet("""
        *{
        background: #fff;
        }
        *:hover{
        background: #f90;
        }
        """)
        
        namew.setFixedWidth(82)
        hlo.addWidget(namew)
        
        for n in xrange(len(colsconfs)-1):
            multbut = itemHeader(colshs[n+1][0], colshs[n+1][1], 16+int(colshs[n+1][2])*4.4, n, self.multAll, self.sumAll, self.setAll, self.highlightCol)
            hlo.addWidget(multbut)
            
        self.setContentsMargins(0, 0, 0, 0)
        
    def multAll(self):
        
        val = QInputDialog.getDouble(self.parent().parent(), "Enter Value", "Value: ", 1, -999999999, 999999999, 2)
        
        if val[1] == True:
            for wid in self.widslist:
                if wid.checkbox.isChecked():
                    col = self.sender().col
                    wid.spinboxes[col].setValue(
                                                wid.spinboxes[col].value() * float(val[0])
                                                )

    def setAll(self):
        val = QInputDialog.getDouble(self.parent().parent(), "Enter Value", "Value: ", 1, -999999999, 999999999, 2)
        
        if val[1] == True:
            for wid in self.widslist:
                if wid.checkbox.isChecked():
                    col = self.sender().col
                    wid.spinboxes[col].setValue((val[0]))
    
    def sumAll(self):
        val = QInputDialog.getDouble(self.parent().parent(), "Enter Value", "Value: ", 1, -999999999, 999999999, 2)
        
        if val[1] == True:
            for wid in self.widslist:
                if wid.checkbox.isChecked():
                    col = self.sender().col
                    wid.spinboxes[col].setValue(
                                                wid.spinboxes[col].value() + float(val[0])
                                                )
    
    def highlightCol(self):
        col = self.sender().col
        for wid in self.widslist:
            c=0
            for spinbox in wid.spinboxes:
                if c == col:
                    spinbox.setStyleSheet("*{background:#f90;}*:hover{background:#ff0}")
                else:
                    spinbox.setStyleSheet("")
                c+=1

class vEdLine(QWidget):
    def __init__(self, data, cstl):
        QWidget.__init__(self)
        
        self.changedstyle = cstl
        
        hlo = QHBoxLayout(self)
        hlo.setContentsMargins(0, 0, 0, 0)
        hlo.setSpacing(0)
        
        self.name = data[0]
        namew = QLabel(self.name)        
        namew.setFixedSize(70,16)
        hlo.addWidget(namew)
        
        self.checkbox = QCheckBox(self)
        self.checkbox.setFixedSize(12,16)
        self.checkbox.setChecked(True)
        hlo.addWidget(self.checkbox)
        
        self.spinboxes = []
        
        intcols = [4,9,34,35,36,37]
        
        c=1
        for prop in data[1:]:
            c+=1
            if c in intcols:
                propw = QSpinBox()
            else:
                propw = QDoubleSpinBox()
                propw.setSingleStep(0.1)
            
            propw.setToolTip(colshs[c-1][1] + "\n" + self.name)
            
            propw.valueChanged.connect(self.highlight)
            
            propw.setMaximum(999999999)
            propw.setMinimum(-999999999)
            propw.setValue(float(prop))    
            propw.setFixedSize(16+int(colshs[c-1][2])*4.4, 16)
            self.spinboxes.append(propw)
            hlo.addWidget(propw)

        hlo.addSpacerItem(QSpacerItem(0,16,QSizePolicy.Expanding,QSizePolicy.Minimum))
    
    def highlight(self):
        self.setStyleSheet(self.changedstyle)
    
    def getLine(self):
        
        line = " "
        
        props = [self.name]
        for sb in self.spinboxes:
            props.append(str(sb.value()))
        
        return line.join(props)

def createButton(text, parent, function, layout):
    newbut = QPushButton(text, parent)
    newbut.clicked.connect(function)
    layout.addWidget(newbut)
    return newbut

class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.setWindowTitle("GTA IV Handling Editor by Wolf from FGReactor")
        
        global restart
        restart = False
        
        self.widslist = []
        
        scroller = QScrollArea(self)
        scrwid = QWidget(self)
        self.scrwid = scrwid
        scroller.setWidget(scrwid)
        scroller.setWidgetResizable(True)
        scrlo = QVBoxLayout()
        scrlo.setContentsMargins(0, 0, 0, 0)
        scrlo.setSpacing(0)
        scrwid.setLayout(scrlo)
        self.mlo = scrlo
        
        startnotice = QLabel("""Use the <b>"Open Handling File" button</b> or the <b>"Recent Files" menu</b> below to start editing.<br><br>
                                Contact: fgreactor@gmail.com
                                
        """)
        startnotice.setStyleSheet("font-size: 16px; padding:40px")
        scrlo.addWidget(startnotice)
        self.startnotice = startnotice
        
        self.openframe = QFrame()
        self.openframe.setStyleSheet("font-size: 16px; font-weight: bold")
        oflo = QVBoxLayout(self.openframe)
        self.openbut = createButton("Open Handling File (Browse)", self.openframe, self.openfile, oflo)

        for rfile in recent:
            if rfile != "":
                but = createButton(rfile, self.openframe, self.openfile, oflo)
                but.recfile = rfile    
        oflo.addSpacerItem(QSpacerItem(30,30,QSizePolicy.Expanding,QSizePolicy.Expanding))
        scrlo.addWidget(self.openframe)
        
        self.errorbut = QFrame()
        self.errorbut.setStyleSheet("font-size: 90px; font-weight: bold; color: #c00; max-width: 400px")
        erlo = QVBoxLayout(self.errorbut)
        createButton(u"OK...", self, self.openAnother, erlo)
        erlo.addSpacerItem(QSpacerItem(30,30,QSizePolicy.Expanding,QSizePolicy.Expanding))
        scrlo.addWidget(self.errorbut)
        self.errorbut.hide()
        
        mainwid = QWidget(self)
        mainlo = QVBoxLayout(mainwid)
        self.setCentralWidget(mainwid)
        mainlo.addWidget(scroller)
        mainlo.setContentsMargins(0, 0, 0, 0)
        
        butslo = QHBoxLayout()
        mainlo.addLayout(butslo)
        
        self.openanotherbut = createButton("Open Another File", self, self.openAnotherConfirm, butslo)
        
        self.selbut = QPushButton("(De)Select All...", self)
        butslo.addWidget(self.selbut)
        
        smenu = QMenu(self)
        
        smenu.addAction("Select All", self.selectAll)
        smenu.addAction("Deselect All", self.deselectAll)
        
        for line in vehiclestypes:
            sact = QAction("Select All "+line[0], self)
            sact.vehicles = line[1:]
            sact.triggered.connect(self.selectAll)
            smenu.addAction(sact)
            dact = QAction("Deselect All "+line[0], self)
            dact.vehicles = line[1:]
            dact.triggered.connect(self.deselectAll)
            smenu.addAction(dact)
        
        self.selbut.setMenu(smenu)
        
        
        self.savebut = createButton("Save File", self, self.savefile, butslo)
        self.saveasbut = createButton("Save File As", self, self.savefileas, butslo)
        
        self.bottombuttons = [self.openanotherbut, self.saveasbut, self.savebut, self.selbut]
        
        for but in self.bottombuttons:
            but.hide()
        
    def selectAllX(self, select, xlist):
            
        for vehicle in self.widslist:
            if xlist == "ALL":
                vehicle.checkbox.setChecked(select)
            else:
                if vehicle.name in xlist:
                    vehicle.checkbox.setChecked(select)

    def selectAll(self):
        try:
            vehiclestoselect = self.sender().vehicles
        except:
            vehiclestoselect = "ALL"
            
        self.selectAllX(True, vehiclestoselect)
        
    def deselectAll(self):
        try:
            vehiclestoselect = self.sender().vehicles
        except:
            vehiclestoselect = "ALL"
            
        self.selectAllX(False, vehiclestoselect)
    
    def savefile(self, xfile=False):
        if xfile == False:
            xfile = self.curfile
            
        try:
            outfile = open(xfile, "w")
                
            for obj in self.linesobjs:
                line = obj.getLine()
                print line
                outfile.write(line)
            
            QToolTip.showText(self.savebut.mapToGlobal(QPoint()), "File Saved Successfully!")
                
                
        except:
            conf = QMessageBox(self)
            conf.setWindowTitle("Error")
            conf.setText("An Error Occurred While Saving the File.\nMake Sure You Have Write Permission.")
            conf.setIcon(QMessageBox.Warning)
            conf.setStandardButtons(QMessageBox.Ok)
            conf.exec_()
        
    def savefileas(self):
        outfile = QFileDialog.getSaveFileName(self, directory=self.curfile, filter="*.dat")
        if(outfile != ""):
            self.savefile(outfile)
        
    
    def openAnother(self):
        global restart
        restart = True
        self.close()
    
    def openAnotherConfirm(self):
        conf = QMessageBox(self)
        conf.setWindowTitle("Close The File Currently Open?")
        conf.setText("Are you sure?\nAll unsaved data in the current file will be lost.")
        conf.setIcon(QMessageBox.Warning)
        conf.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
        res = conf.exec_()
        
        if res == QMessageBox.Ok:
            self.openAnother()
    
    def openfile(self):
        
        try:
            xfile = self.sender().recfile
        except:
            lastfile = "C:\\"
            
            if len(recent) > 0:
                lastfile = recent[-1]
            xfile = QFileDialog.getOpenFileName(self, directory=lastfile, filter="*.dat")
        
        if xfile == "":
            return
        
        if xfile not in recent:
            recentout.write(xfile+"\n")
        
        self.openframe.hide()
        self.openframe.deleteLater()
        
        self.startnotice.setText("<b>LOADING FILE...</b>")
        self.startnotice.repaint()
        
        self.loadfile(xfile)
    
    def loadfile(self, xfile):

        headerwid = None
        widslist = []
        
        try:

            infile = open(xfile)
        
            hlines = []
            self.linesobjs = hlines
            
            headerwid = hHLine(widslist)
            self.mlo.addWidget(headerwid)
            
            c=1
        
            for line in infile:
                hlines.append(lineData(line, self.mlo, widslist))
                self.startnotice.setText("<b>LOADING FILE - "+str(c)+" LINES ANALYZED</b>")
                self.startnotice.repaint()
                c+=1
            
            self.mlo.addSpacerItem(QSpacerItem(30,30,QSizePolicy.Expanding,QSizePolicy.Expanding))
            
            self.startnotice.setText("<b>LOADING FILE - POPULATING GUI...</b>")
            self.startnotice.repaint()
                
            self.widslist = widslist
            
            self.scrwid.setStyleSheet(scrwidss)
            
            self.startnotice.close()
            self.startnotice.deleteLater()
            
            self.curfile = xfile
            
            for but in self.bottombuttons:
                but.show()
            
        except:
            self.startnotice.setText(self.startnotice.text()+"<br><b style=\"color:red\">ERROR LOADING FILE!!!</b><br>Please, make sure the file is valid.")
            
            self.errorbut.show()
            
            if headerwid is not None:
                headerwid.hide()
            
            for wid in widslist:
                wid.hide()
                


def main():
    
    app = QApplication([])

    mainw = Main()
    mainw.showMaximized()
    
    app.exec_()

if __name__ == '__main__':
    
    restart = True
    
    while restart:
        
        scrrow = 0
        colsconfs = []
        recent = []
        
        specialvehicles = []
        forbtags = []
        vehiclestypes = []
        recentout = open("recent", "a")
        
        try:
            forbtags = open("forbiddentags").readline().split()
            colsconfs = open("cols").readlines()
            recent = open("recent").read().split("\n")
            recent.remove("")
            spcfile = open("specialvehicles").readlines()
            vtypes = open("vehiclestypes").readlines()
             
            for line in spcfile:
                for entry in line.split():
                    specialvehicles.append(entry)
                    
            for line in vtypes:
                vehiclestypes.append(line.split())
            
            
            
        except:
            pass
        
        
        colshs = []
        for line in colsconfs:
            colshs.append(line.split())
        
        main()
    
