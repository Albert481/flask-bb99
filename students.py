class Students:
    def __init__(self, name, squad):
        self.__trolleyid = ''
        self.__name = name
        self.__squad = squad
        # self.__count = count
        # self.__location = location
        # self.__comments = comments

    def get_name(self):
        return self.__name
    def get_squad(self):
        return self.__squad
    # def get_count(self):
    #     return self.__count
    # def get_location(self):
    #     return self.__location
    # def get_comments(self):
    #     return self.__comments
    # def get_trolleyid(self):
    #     return self.__trolley
    def set_trolleyid(self, trolleyid):
        self.__trolleyid = trolleyid