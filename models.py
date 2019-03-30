class Students:
    def __init__(self, studId, studClass, studName, studSquad):
        self.__studId = studId
        self.__studClass = studClass
        self.__studName = studName
        self.__studSquad = studSquad

    def get_studId(self):
        return self.__studId

    def get_studName(self):
        return self.__studName

    def get_studClass(self):
        return self.__studClass

    def get_studSquad(self):
        return self.__studSquad

class Attendance(Students):
    def __init__(self, studId, studClass, studName, studSquad, attendancy, date):
        super().__init__(studId, studClass, studName, studSquad)
        self.__date = date
        self.__attendancy = attendancy

    def get_attendancy(self):
        return self.__attendancy

    def set_attendancy(self, status):
        self.__attendancy = status

    def get_date(self):
        return self.__date

