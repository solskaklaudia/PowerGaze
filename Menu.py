class Menu:

    def __init__(self,name):

        self.name = name
        self.visible = False


    def show(self):
        self.visible = True


    def hide(self):
        self.visible = False