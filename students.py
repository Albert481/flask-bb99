class Students:
    def __init__(self, name, sclass, squad, slevel, tattend):
        self.__name = name
        self.__sclass = sclass
        self.__squad = squad
        self.__slevel = slevel
        self.__tattend = tattend
        # self.__location = location
        # self.__comments = comments

    def get_name(self):
        return self.__name
    def get_squad(self):
        return self.__squad
    def get_level(self):
        return self.__slevel
    def get_tattend(self):
        return self.__tattend
    def get_sclass(self):
        return self.__sclass
    # def get_comments(self):
    #     return self.__comments
    # def get_trolleyid(self):
    #     return self.__trolley

class Infractions(Students):
    def __init__(self,name, sclass, squad, slevel, tattend, infractioncount):
        super().__init__(name, sclass, squad, slevel, tattend)
        self.__infractioncount = infractioncount

    def get_infractioncount(self):
        return self.__infractioncount