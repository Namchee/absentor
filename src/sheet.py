from gspread_formatting import CellFormat, TextFormat, format_cell_range

class Sheet:
    def __init__(self, worksheet):
        self.worksheet = worksheet

        if self.__is_sheet_empty():
            self.__initialize_sheet()

    """Check if the current sheet hasn't been prefilled
    """
    def __is_sheet_empty(self):
        return not self.worksheet.cell(1, 1).value

    """Fill the spreadsheet with basic headers
    """
    def __initialize_sheet(self):
        self.worksheet.update_cell(1, 1, 'NPM')
        self.worksheet.update_cell(1, 2, 'Nama')

        self.__bold_headers()

    """Get the farthest non-empty column index
    """
    def __get_highest_column(self, row = 1):
        highest_column = 1

        while (self.worksheet.cell(row, highest_column).value):
            highest_column += 1

        return highest_column

    """Get the farthest non-empty row index
    """
    def __get_highest_row(self, column = 1):
        highest_row = 1

        while (self.worksheet.cell(highest_row, column).value):
            highest_row += 1

        return highest_row

    """Bold sheet headers
    """
    def __bold_headers(self):
        fmt = CellFormat(
            textFormat=TextFormat(bold=True)
        )

        format_cell_range(self.worksheet, "1", fmt)

    """Mark user's presence by name
    
    Params:
        - date {datetime}: Date object which defines the current date
        - name {string}: Username
    """
    def absen(self, date, name):
        return