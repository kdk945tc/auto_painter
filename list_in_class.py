class NewList:
    def __init__(self, arg1,arg,*arg):
        self.arg = arg
        self.arg1 = arg1

    def printArg(self):
        print(self.arg)
        for i in self.arg:
            print(i)

a = NewList(1,2,3,4,5)
a.printArg()