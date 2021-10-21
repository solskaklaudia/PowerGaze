class Screen:

    def __init__(self):

        self.zoom = 1           # screen zoom multiplier
        self.zoom_pos = [0,0]   # top left coordinates of zoomed area


    def zoomIn(self, zoom_pos):
        self.zoom += 1
        self.zoom_pos = zoom_pos


    def zoomOut(self):
        self.zoom = 1
        self.zoom_pos = [0,0]