from gspread_formatting import CellFormat, TextFormat, format_cell_ranges

class Sheet:
    def __init__(self, spreadsheet, worksheet):
        self.spreadsheet = spreadsheet
        self.worksheet = worksheet

        if self.__is_sheet_empty():
            self.__initialize_sheet()

    """Check if the current sheet hasn't been prefilled

        Return: {boolean} True if the sheet is empty, False otherwise
    """
    def __is_sheet_empty(self):
        return not self.worksheet.cell(1, 1).value

    """Fill the spreadsheet with basic headers
    """
    def __initialize_sheet(self):
        self.worksheet.update_cell(1, 1, 'NPM')
        self.worksheet.update_cell(1, 2, 'Nama')

        self.__format_headers()

    """Get the farthest non-empty column index (inclusive)

        Return: {int} The farthest non-empty row-index
    """
    def __get_highest_column(self, row = 1):
        highest_column = 1

        while (self.worksheet.cell(row, highest_column).value):
            highest_column += 1

        return highest_column - 1

    """Get the farthest non-empty row index (inclusive)

        Return: {int} The farthest non-empty row-index
    """
    def __get_highest_row(self, column = 1):
        highest_row = 1

        while (self.worksheet.cell(highest_row, column).value):
            highest_row += 1

        return highest_row - 1

    """Stolen from StackOverflow
        https://stackoverflow.com/questions/23861680/convert-spreadsheet-number-to-column-letter
    """
    def __colnum_string(self, n):
        string = ""
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            string = chr(65 + remainder) + string

        return string

    """Formats the presence mark
    """
    def __format_mark(self):
        # Mark Formatting (centered 'X')
        mark_format = CellFormat(
            horizontalAlignment="CENTER"
        )

        format_cell_ranges(self.worksheet, [
            ("C2:{}{}".format(
                self.__colnum_string(self.__get_highest_column()),
                self.__get_highest_row()
            ), mark_format)
        ])

    """Formats the table headers
    """
    def __format_headers(self):
        # Header format (centered and bold)
        header_format = CellFormat(
            textFormat=TextFormat(bold=True),
            horizontalAlignment="CENTER"
        )

        format_cell_ranges(self.worksheet, [
            ("1", header_format)
        ])

    """Formats the table's data with standard style
    """
    def __format_data(self):
        # NPM Formatting (right-aligned)
        npm_format = CellFormat(
            horizontalAlignment="RIGHT"
        )

        # Name Formatting (left-aligned)
        name_format = CellFormat(
            horizontalAlignment="LEFT"
        )

        format_cell_ranges(self.worksheet, [
            ("A2:A", npm_format),
            ("B2:B", name_format)
        ])

        # Do column resizing, sorting, and bordering after update
        body = {
            "requests": [
                {
                    "autoResizeDimensions": {
                        "dimensions": {
                            "sheetId": 0,
                            "dimension": "COLUMNS",
                            "startIndex": 0,
                            "endIndex": self.__get_highest_column()
                        }
                    },
                },
                {
                    "updateBorders": {
                        "range": {
                            "sheetId": 0,
                            "startRowIndex": 0,
                            "endRowIndex": self.__get_highest_row(),
                            "startColumnIndex": 0,
                            "endColumnIndex": self.__get_highest_column()
                        },
                        "top": {
                            "style": "SOLID"
                        },
                        "left": {
                            "style": "SOLID"
                        },
                        "right": {
                            "style": "SOLID"
                        },
                        "bottom": {
                            "style": "SOLID"
                        },
                        "innerVertical": {
                            "style": "SOLID"
                        },
                        "innerHorizontal": {
                            "style": "SOLID"
                        },
                    }
                }
            ]
        }

        self.spreadsheet.batch_update(body)

    """
        Find the index of a date
        If not found, this function will create it first
        
        Params:
            - date {date}: Date object which defines the current date.
            Must be a pyhton `date` object
        Return: Tuple(row, column)
    """
    def __get_date_index(self, date):
        date_format = date.strftime("%d/%m")
        cell = self.worksheet.findall(date_format)

        # If the cell doesn't exist, create it
        if len(cell) == 0:
            column_index = self.__get_highest_column() + 1

            self.worksheet.update_cell(1, column_index, date_format)
            self.__format_headers()

            column = column_index
        else:
            column = cell[0].col

        return (1, column)

    """
        Find the index of a mahasiswa
        If not found, this function will create it first
        
        Params:
            - npm {string}: NPM Mahasiswa
            - name {string}: Nama Mahasiswa
        Return: Tuple(row, column)
    """
    def __get_mahasiswa_index(self, npm, name):
        cell = self.worksheet.findall(npm)

        # If the cell doesn't exist, create it
        if len(cell) == 0:
            row_index = self.__get_highest_row(2) + 1

            self.worksheet.update_cell(row_index, 1, npm)
            self.worksheet.update_cell(row_index, 2, name.upper())

            row = row_index
        else:
            row = cell[0].row

        return (row, 1)


    """Mark mahasiswa's presence by name
    
        Params:
            - date {date}: Date object which defines the current date.
            Must be a pyhton `date` object
            - npm {string}: NPM Mahasiswa
            - name {string}: Nama Mahasiswa
    """
    def __absen(self, date, npm, name):
        _, column = self.__get_date_index(date)
        row, _ = self.__get_mahasiswa_index(npm, name)

        self.worksheet.update_cell(row, column, "X")

    """Do a batched presence marking (commit many operations at once)

        Params:
            - date {date}: Date object which defines the current date.
            Must be a pyhton `date` object
            - mahasiswas {list}: List of Mahasiswa
    """
    def batch_absen(self, date, mahasiswas):
        for mahasiswa in mahasiswas:
            self.__absen(date, mahasiswa.npm, mahasiswa.name)

        self.__format_mark()
        self.__format_data()

    """Mark mahasiswa's presence by name
        Only use this method if you only want to update ONE instance.
        If you want to update many mahasiswa at once, use `batch_absen`
    
        Params:
            - date {date}: Date object which defines the current date.
            Must be a pyhton `date` object
            - mahasiswa {Mahasiswa}: Mahasiswa object
    """
    def absen(self, date, mahasiswa):
        self.__absen(date, mahasiswa.npm, mahasiswa.name)

        self.__format_mark()
        self.__format_data()
