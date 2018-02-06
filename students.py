class Students:
    def __init__(self, name, squad):
        self.__name = name
        self.__squad = squad
        self.__tattend = '0'
        # self.__location = location
        # self.__comments = comments

    def get_name(self):
        return self.__name
    def get_squad(self):
        return self.__squad
    def get_tattend(self):
        return self.__tattend
    # def get_location(self):
    #     return self.__location
    # def get_comments(self):
    #     return self.__comments
    # def get_trolleyid(self):
    #     return self.__trolley