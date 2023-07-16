class SymbolTable:
    def __init__(self):
        self.table = {}

    def insert(self, identifier, attributes):
        hash_value = self._hash(identifier)
        if hash_value in self.table:
            # Handle collision by chaining (using a linked list)
            self.table[hash_value].append((identifier, attributes))
        else:
            self.table[hash_value] = [(identifier, attributes)]

    def lookup(self, identifier):
        hash_value = self._hash(identifier)
        if hash_value in self.table:
            entries = self.table[hash_value]
            for entry in entries:
                if entry[0] == identifier:
                    return entry[1]  # Return the attributes
        return None  # Identifier not found

    def update_attributes(self, identifier, new_attributes):
        hash_value = self._hash(identifier)
        if hash_value in self.table:
            entries = self.table[hash_value]
            for i, entry in enumerate(entries):
                if entry[0] == identifier:
                    entries[i] = (identifier, new_attributes)
                    return True  # Attribute updated successfully
        return False  # Identifier not found or attribute not updated

    def print_table(self):
        for hash_value in self.table:
            entries = self.table[hash_value]
            for entry in entries:
                print(f"Variable: {entry[0]}, Attributes: {entry[1]}")

    def _hash(self, identifier):
        # Simple hash function using Python's built-in hash function
        return hash(identifier)


# Example usage: ---------------------------------------------------------
'''
symbol_table = SymbolTable()

# Inserting identifiers with attributes into the symbol table
symbol_table.insert("x", {"type": "int", "value": 10})
symbol_table.insert("y", {"type": "float", "value": 3.14})
symbol_table.insert("z", {"type": "string", "value": "Hello"})

# Update attributes of an identifier
if symbol_table.update_attributes("x", {"type": "float", "value": 3.5}):
    print("Attributes of 'x' updated successfully")
else:
    print("'x' not found in the symbol table")

# Print the entire symbol table
symbol_table.print_table()
'''
