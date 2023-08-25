import os
from datetime import date
from os import scandir

class Controller:
    def __init__(self) -> None:
        self.projectPath =  str(os.path.dirname(os.path.abspath(__file__)))
        self.diasDeLaSemana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
        self.output = {} # Save response [day][hour] = [#, id]
        self.dayOfWeek = {} # Save [day][hour] = activity 
        for i in self.diasDeLaSemana:
            self.dayOfWeek[i] = {}
            self.output[i] = {}

    def loadAllData(self):
        """
        Read All folder in DATA
        then read all subpath in DATA to extract txt info
        save the info in self.data[time] = information
        """
        folders = self._listALLFolderInPath(f"{self.projectPath}\\DATA")
        
        for x in folders:
            for y in self._listAllFilesTXTInPath(f"{self.projectPath}\\DATA\\{x}"):
                _date = str(y).replace(".txt", "")
                _date = _date.split(" ")
                _date = self._getNameOfDayByDate(_date)
                _day = self._getTextInFile(f"{self.projectPath}\\DATA\\{x}\\{y}")
                for z in _day.split("\n"):
                    if z.strip() == "":
                        continue
                    _hour = z.split(":")[0] # Cacth the hour of event
                    _activity = z.split(":")[1] # Cacth the value
                    if _hour not in self.dayOfWeek[_date].keys():
                        self.dayOfWeek[_date][_hour] = {}
                    
                    if _activity not in self.dayOfWeek[_date][_hour].keys():
                        self.dayOfWeek[_date][_hour][_activity] = 0

                    self.dayOfWeek[_date][_hour][_activity] = self.dayOfWeek[_date][_hour][_activity] + 1

        # Save LOG
        with open("LOGs/log.data.charge.log", "w", encoding="UTF-8") as f:
            f.write(str(self.dayOfWeek))


    def ShortedDataByDay(self):
        for x in self.diasDeLaSemana: # Get a day of week
            for y in self.dayOfWeek[x]: # get the hour of this day
                if y not in self.output[x].keys():
                    self.output[x][y] = ""
                self.output[x][y] = self._getMostTopInDayXHour(self.dayOfWeek[x][y])

        # Save LOG
        with open("LOGs/log.data.top.log", "w", encoding="UTF-8") as f:
            f.write(str(self.output))


    def showDataConvergencyByHourOfDay(self):
        _data = ""
        for i in self.output:
            _data = _data + f"============{i}================\n"
            for j in self.output[i]:
                _data = _data + f"{j}>>{self.output[i][j]}\n"
            _data = _data + "\n"

        print(_data)
        # Save LOG
        with open("LOGs/log.data.top.response.log", "w", encoding="UTF-8") as f:
            f.write(_data) 


    def _getMostTopInDayXHour(self, data):
        """
        Enter a {'a': x, 'b': y, 'c': z} and return the highest key
        """
        comparator = 0
        key = ""
        for i in data:
            if data[i] > comparator:
                comparator = data[i]
                key = i
        
        return key

    def _listALLFolderInPath(self, path):
        """
        Enter a x/y/z and return ['Folder1',... 'FolderN']
        """
        folders = []

        try:
            for i in scandir(path):
                if i.is_dir():
                    folders.append(i.name)
        except:
            pass

        return folders
    

    def _listAllFilesTXTInPath(self, ruta):
        """
        Retorna el nombre de todos los archivos.extension de una carpeta
        """
        _filesNames = []
        
        try:
            for i in scandir(ruta):
                if i.is_file():
                    if ".txt" in i.name:
                        _filesNames.append(i.name)
        except:
            pass

        return _filesNames
    

    def _getTextInFile(self, filepath):
        with open(filepath, "r", encoding="UTF-8") as f:
            return f.read()
        
        
    def _getNameOfDayByDate(self, d):
        """
        Enter a date [YYYY, MM, DD] and return a name of day
        """
        day = ""

        try:
            _d = date(int(d[0]), int(d[1]), int(d[2]))
            _d = _d.weekday()
            day = self.diasDeLaSemana[_d]
        except:
            pass

        return day