class Cursor:

    coordinates = [0,0]     # calculated cursor coordinates
    min_difference = 50     # minimal difference for cursor to move
    stationary_counter = 0  # counter for how many frames cursor remained stationary

    def setCursorPosition(self, cursor_x, cursor_y, screen_width, screen_height):
        """ Calculates cursor position on the screen """

        # Edge cases
        if(cursor_x < 0.0):
            cursor_x = 0.0
        if (cursor_x >= screen_width):
            cursor_x = screen_width-1
        if(cursor_y < 0.0):
            cursor_y = 0.0
        if (cursor_y >= screen_height):
            cursor_y = screen_height-1

        # Set cursor position only when difference is big enough
        x_diff = abs(self.coordinates[0] - cursor_x)
        y_diff = abs(self.coordinates[1] - cursor_y)

        if(x_diff >= self.min_difference):
            self.coordinates[0] = cursor_x
            self.stationary_counter = 0

        if(y_diff >= self.min_difference):
            self.coordinates[1] = cursor_y
            self.stationary_counter = 0
