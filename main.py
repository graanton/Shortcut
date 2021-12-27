from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from windowUI.UI_v5 import Ui_MainWindow
from add_game_window import TableInfo
import json
from os.path import isfile
from functools import partial
from os import startfile,chdir,getcwd
from time import sleep as wait
class Update(QObject):
    about_new_log = pyqtSignal()
    get_path=None
    def run(self,file='games.json'):
        path=self.get_path+'\\'+file
        while True:
            try:
                self.about_new_log.emit()
            except:print("XD")
            wait(0.1)
class ShortCut(Ui_MainWindow,QMainWindow):
    def __init__(self):
        super(ShortCut, self).__init__()

        self.start_path = getcwd()
        self.setupUi(self)
        self.setWindowIcon(QIcon('res\\icon.png'))
        self.setWindowTitle('AntonPog')
        self.re = None
        self.SetupButtons()
        self.setup_table_info()



        try:
            self.thread = QThread()
            self.data_reset=Update()
            self.data_reset.get_path = self.start_path
            self.data_reset.moveToThread(self.thread)
            self.data_reset.about_new_log.connect(self.SetupButtons)
            self.thread.started.connect(self.data_reset.run)
            self.thread.start()
            print('started')
        except:print('>:')
        self.pushButton.setText('Изменить')




    def SetupButtons(self,):

        game_info = self.get_json_list()
        if self.re != game_info:
            self.delete_side(self.verticalLayout)


            game_names=self.get_game_names(game_info)
            self.re=game_info
            game_start_buttons = []

            for num in range(len(game_names)):
                game_start_buttons.append(QPushButton())
            numGame=0
            for button in game_start_buttons:
                game=game_names[numGame]
                comand_add=partial( self.rename,
                    game,
                    game_info[game]['description'],
                    partial(self.start_file,game_info[game]['path'])
                )
                button.clicked.connect(comand_add)
                button.setText(game)
                self.verticalLayout.addWidget(button)
                numGame+=1
            self.re= game_info

    def delete_side(self,obj):
        while obj.count():
            item=obj.takeAt(0)
            widget = item.widget()
            if widget != None:
                widget.deleteLater()

    def get_game_names(self,json_file={}):
        games_list=[]
        for game_name in json_file.keys():
            games_list.append(game_name)
        return games_list
    def get_json_list(self,path=None,gamelist={}):
        path=self.start_path+'\\games.json'
        game_dict=gamelist
        if gamelist!={} :
            game_dict=gamelist
        else:
            if isfile(path)==True:
                with open (path) as file:
                    game_dict=json.load(file) #default

            else:
                with open(path,'w') as file:
                    json.dump(gamelist,file,indent=2)
        return game_dict
    def rename(self,heading='Название',disctiption='Описание: Антон топ.',comand=None):

        self.name.setText(heading)
        self.label.setText(disctiption)
        try:self.pushButton_4.clicked.disconnect()
        except:pass
        self.pushButton_4.clicked.connect(comand)
    def start_file(self,path):
        path=path.replace('/','\\')
        exe_file=''
        puth=''
        for i in range(len(path)):
            if '\\' not in path[i:]:
                exe_file+=path[i]
            else:
                puth+=path[i]
        chdir(puth)
        startfile(exe_file)
    def setup_table_info(self):
        self.ti = TableInfo()
        need_dict=self.get_json_list()
        for name in need_dict.keys():
            self.ti.add_line(
                name,
                need_dict[name]['description'],
                need_dict[name]['path']
            )
        self.ti.json_dict = self.get_json_list()
        self.pushButton.clicked.connect(lambda: self.ti.show())

    def test(self):
        print(":)")







if __name__ == '__main__':
    app = QApplication([])
    sc=ShortCut()
    sc.show()
    app.exec_()
