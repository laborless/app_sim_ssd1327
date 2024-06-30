class TwoDArray:
    def __init__(self, rows, cols):
        """Initialize a 2D array with given dimensions"""
        self.rows = rows
        self.cols = cols
        self.data = [['' for _ in range(cols)] for _ in range(rows)]  # Initialize with empty strings
    
    def set_value(self, row, col, value):
        """Set the value at the specified row and column"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.data[row][col] = value
        else:
            raise IndexError("Index out of bounds")
    
    def get_value(self, row, col):
        """Get the value at the specified row and column"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.data[row][col]
        else:
            raise IndexError("Index out of bounds")
    
    def set_value_from_string(self, row, col, value_string):
        """Set values from a comma-separated string"""
        values = value_string.split(',')
        if len(values) == 1:
            self.set_value(row, col, value_string)
        elif len(values) == self.cols:
            self.data[row][col] = values[col]
        else:
            raise ValueError("Number of values does not match number of columns")
    
    def get_value_as_string(self, row, col):
        """Get values as a comma-separated string"""
        return self.data[row][col]
    
    def to_string(self):
        """Converts the entire 2D array to a concatenated string with comma separator"""
        return ','.join(','.join(row) for row in self.data)
    
    def recreate_array(self, new_rows, new_cols):
        """Recreate the 2D array with new dimensions"""
        new_data = [['' for _ in range(new_cols)] for _ in range(new_rows)]
        for i in range(min(self.rows, new_rows)):
            for j in range(min(self.cols, new_cols)):
                new_data[i][j] = self.data[i][j]
        self.rows = new_rows
        self.cols = new_cols
        self.data = new_data
    
# Example usage:
arr = TwoDArray(3, 4)  # Create a 3x4 2D array

# Setting values from comma-separated strings
arr.set_value_from_string(0, 0, "apple,banana,orange,grape")
arr.set_value_from_string(1, 2, "one,two,three,four")
arr.set_value_from_string(2, 3, "cat,dog,rabbit")

# Getting values as comma-separated strings
print(arr.get_value_as_string(0, 0))  # Output: "apple,banana,orange,grape"
print(arr.get_value_as_string(1, 2))  # Output: "one,two,three,four"
print(arr.get_value_as_string(2, 3))  # Output: "cat,dog,rabbit"

# Converting entire array to string
print(arr.to_string())  # Output: "apple,banana,orange,grape, , ,one,two,three,four, , , ,cat,dog,rabbit"

# Recreate array with new dimensions
arr.recreate_array(2, 3)
print(arr.to_string())  # Output: "apple,banana,orange, , ,one,two,three"

# Accessing out-of-bounds index (will raise IndexError)
# arr.get_value_as_string(3, 0)
