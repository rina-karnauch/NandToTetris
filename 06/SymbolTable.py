##########################################
# name: Rina Karnauch, username: rina.karnauch
# name : Eynam Wassertheil, username: came1337
##########################################

class SymbolTable:
    """
    a symbol table class.
    a decorator table for 2 main tables:
    1 - table of labels.
    2 - table of variables + predefines variables.
    """

    def __init__(self):
        """
        construction of symbol table class.
        """
        #  different dictionary of different kind of symbols
        self.table = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
                      "SCREEN": 16384, "KBD": 24576, "R0": 0, "R1": 1,
                      "R2": 2, "R3": 3, "R4": 4, "R5": 5,
                      "R6": 6, "R7": 7, "R8": 8, "R9": 9, "R10": 10,
                      "R11": 11, "R12": 12, "R13": 13, "R14": 14,
                      "R15": 15}
        self.taken_addresses = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                                14, 15, 16384,
                                24576]
        self.create_keys()
        self.keys = None

    def create_keys(self):
        """
        #  helper method to the instructor of the symbol table
        :return: none
        """
        self.keys = list(self.table)

    def clear(self):
        """
        clear method for the symbol table
        :return: none
        """
        self.table.clear()

    def is_occupied(self, address: int):
        """
        method to check weather an address is already occupied or not
        :param address: wanted address
        :return: True for taken False otherwise
        """
        if address in self.taken_addresses:
            return True
        return False

    def add_entry(self, symbol: str, address: int):
        """
        ** we already know that address is not taken **
        Adds the pair (symbol, address) to the table.
        :param symbol: the symbol to add to the table
        :param address: the address to add it to
        :return: none
        """
        if self.contains(symbol):
            # already in
            return
        self.table[symbol] = address
        self.taken_addresses.append(address)

    def add_label(self, symbol: str, address: int):
        """
        ** we already know that address is not taken **
        Adds the pair (symbol, address) to the table.
        :param symbol: the symbol to add to the table
        :param address: the address to add it to
        :return: none
        """
        if self.contains(symbol):
            # already in
            return
        self.table[symbol] = address

    def contains(self, symbol: str):
        """
        Does the symbol table contain the given symbol?
        :param symbol: symbol to check if exists
        :return: true for contains, false otherwise
        """
        if symbol in self.table.keys():
            return True
        return False

    def get_address(self, symbol: str):
        """
        Returns the address associated with the symbol.
        :param symbol: symbol to get address of
        :return: int of address of symbol, None otherwise
        """
        if symbol in self.table.keys():
            return self.table.get(symbol)
        else:
            return None