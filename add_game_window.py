from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from windowUI.DialogWindow import Ui_MainWindow
import json
from functools import partial
from os import getcwd
from windowUI.form import Ui_Form

class TableInfo(Ui_MainWindow,QMainWindow):
    def __init__(self):
        super(TableInfo, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Измена параметров приложений')

        self.json_dict={}
        self.path=getcwd()
        self.setWindowIcon(QIcon(self.path+'\\res\\icon.png'))

        self.lines=[]
        self.add.clicked.connect(lambda : self.add_line())
        self.pushButton.setText('сохранить')
        self.pushButton.clicked.connect(lambda :self.save())
        self.add.setText('добавить')
        for name in self.json_dict.keys():
            self.add_line(name,self.json_dict[name]['description'],self.json_dict[name]['path'])
    def add_line(self,name='unnamed',dis='trash',path='/'):
        line = Ui_Form()
        line.setupUi(self.scrollAreaWidgetContents)
        line.game_name_linedit.setText(name)
        line.description_linedit.setText(dis)
        line.path_linedit.setText(path)
        line.pushButton.clicked.connect(partial(self.delete,line.main_form_layout,len(self.lines)))
        line.path_button.clicked.connect(lambda :self.add_path(line.path_linedit))
        self.verticalLayout_2.addLayout(line.main_form_layout)
        n=0
        list_in=[]

        for in_list in self.lines:
            list_in.append(in_list[1])
        while True:
            if n not in list_in:

                self.lines.append([line,n])
                break
            n+=1

    def add_path(self,linedit):
        file, _ = QFileDialog.getOpenFileName(self, 'Open File', './')
        file=file.replace('/','\\')
        if file[0]==getcwd()[0]:
            linedit.setText(file[2:])
        else:
            linedit.setText(file)
    def delete(self,line,id_line):
        while line.count():
            item=line.takeAt(0)
            widget = item.widget()
            if widget != None:
                widget.deleteLater()
            else:
                self.delete(item.layout())
        index=0
        for i in self.lines:
            if i[1]==id_line:

                self.lines.pop(index)
                break

            index+=1


    def save(self):

        path=self.path + '\\games.json'

        data_before= {}
        for item in range(len(self.lines)):
            item=self.lines[item][0]
            name=item.game_name_linedit.text()
            descrip = item.description_linedit.text()
            path_game = item.path_linedit.text()
            data_before[name]={"description":descrip,"path":path_game}

        with open(path,'w') as file:
            json.dump(data_before,file,indent=2)

        self.json_dict=data_before
if __name__ == '__main__':
    app = QApplication([])
    ti=TableInfo()
    ti.show()
    app.exec_()