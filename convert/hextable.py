""" Hexadecimal table generator for C/C++ projects """

import sys

class HexTable:
    """
    Class to assist with generating arrays of hexadecimal data for C/C++ code.
    This ONLY formats values and ends the array. The array declaration itself
    MUST first be output by the parent code. This is on purpose and by design,
    as the parent code most likely has context-specific information such as
    variable type, sign, or platform-specific modifiers like Arduino's PROGMEM.
    """

    def __init__(self, count, columns=12, digits=2):
        """
        Constructor - initializes counters, etc. for the write() function.
        @param count   Expected number of elements in the array to be
                       generated (so the code knows when to stop appending
                       commas to each element and close the array with ' };')
        @param columns Number of columns (hexadecimal values per line) in
                       the formatted output. Default is 12 (works well for
                       2-digit hex values...under 80 characters/line).
        @param digits  Number of hex digits per value (e.g. 2 for uint8_t,
                       4 for uint16_t, etc.). Default is 2.
        """
        self.limit = count     # Total number of elements in array
        self.counter = 0       # Current array element number (0 to limit-1)
        self.digits = digits   # Digits per array element (after 0x)
        self.columns = columns # Max number of elements before line wrap
        self.column = columns  # Current column number, 0 to columns-1
        # column is initialized to columns to force first-line indent

    def write(self, value):
        """
        Output a single hexadecimal value (with some formatting for C array)
        to standard output.
        @param value Numeric value to write, will be converted to hexadecimal.
                     NO RANGE CHECKING IS PERFORMED, value MUST be within
                     valid range for the constructor's digits setting.
        """
        if self.counter > 0:
            sys.stdout.write(',')                # Comma-delimit prior item
            if self.column < (self.columns - 1): # If not last item on line,
                sys.stdout.write(' ')            # append space after comma
        self.column += 1                         # Increment column number
        if self.column >= self.columns:          # Max column exceeded?
            sys.stdout.write('\n  ')             # Line wrap, indent
            self.column = 0                      # Reset column number
        sys.stdout.write(                        # 0xNN format
            '{0:#0{1}X}'.format(value, self.digits + 2).replace('X', 'x'))
        self.counter += 1                        # Increment item counter
        if self.counter >= self.limit:
            print(' };')                         # Cap off table

    def reset(self, count=0):
        """
        'Recycle' an existing HexTable to start a new one with the same
        number of columns and digits (and item count, if passed).
        @param count Expected number of elements in the new array to be
                     generated. Default of 0 means use same count as before.
        """
        if count > 0:
            self.limit = count
        self.counter = 0
        self.column = self.columns # Init to force first-line indent
