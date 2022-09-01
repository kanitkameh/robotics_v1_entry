class Corner:
    def __eq__(self, other: object) -> bool:
        return self.row == other.row and self.column == other.column

    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

