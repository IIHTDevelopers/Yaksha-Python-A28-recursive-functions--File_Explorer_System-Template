"""
File System Explorer

This module provides functions for recursively exploring file systems,
searching for files, and analyzing file metadata.
"""

# Sample file system structure for demonstration
def create_sample_file_system():
    """
    Create a sample file system structure for demonstration purposes.
    
    Returns:
        dict: A dictionary representing a file system structure with sizes
    """
    return {
        "Documents": {
            "Projects": {
                "project1.docx": 2500000,
                "project2.docx": 1800000,
                "notes.txt": 15000,
                "data.csv": 350000,
            },
            "Personal": {
                "resume.pdf": 520000,
                "budget.xlsx": 480000,
                "Photos": {
                    "vacation.jpg": 3500000,
                    "family.jpg": 2800000,
                    "graduation.png": 4200000,
                }
            },
            "report.pdf": 750000,
        },
        "Downloads": {
            "program.exe": 15000000,
            "Library": {
                "book1.pdf": 12000000,
                "book2.pdf": 9500000,
            },
            "song.mp3": 8000000,
            "video.mp4": 35000000,
        },
        "temp.txt": 2000,
    }

# Directory traversal functions
def list_all_files(directory, file_system=None, path_prefix=""):
    """
    Recursively list all files in a directory structure.
    
    Args:
        directory (str): The directory to list files from
        file_system (dict): The simulated file system structure
        path_prefix (str): Path prefix for constructing full file paths
        
    Returns:
        list: List of all file paths in the directory structure
        
    Base case:
        When we reach a file (value is an integer representing size)
        
    Recursive case:
        When we encounter a directory (dict), process each item inside it
    """
    # Use the sample file system if none provided
    if file_system is None:
        file_system = create_sample_file_system()
    
    # Check if file_system is a valid dictionary
    if not isinstance(file_system, dict):
        raise TypeError("File system must be a dictionary")
    
    # TODO: Implement the recursive directory traversal logic
    # You should handle different cases such as:
    # 1. If directory is specified, navigate to that directory first
    # 2. Process all files in the current directory
    # 3. For each subdirectory, call list_all_files recursively
    # 4. Return a list of all file paths found
    
    # Placeholder return
    return []

def calculate_directory_size(directory, file_system=None):
    """
    Recursively calculate the total size of all files in a directory.
    
    Args:
        directory (str): The directory to calculate size for
        file_system (dict): The simulated file system structure
        
    Returns:
        int: Total size in bytes of all files in the directory
        
    Base case:
        When we reach a file (value is an integer representing size)
        
    Recursive case:
        When we encounter a directory (dict), sum the sizes of all its contents
    """
    # Use the sample file system if none provided
    if file_system is None:
        file_system = create_sample_file_system()
    
    # Check if file_system is a valid dictionary
    if not isinstance(file_system, dict):
        raise TypeError("File system must be a dictionary")
    
    # TODO: Implement the recursive size calculation logic
    # You should handle different cases such as:
    # 1. If directory is specified, navigate to that directory first
    # 2. If we reach a file (integer), return its size
    # 3. If we reach a directory, recursively calculate the size of all its contents
    # 4. Return the total size
    
    # Placeholder return
    return 0

def find_by_extension(directory, extension, file_system=None, path_prefix=""):
    """
    Recursively find all files with a specific extension.
    
    Args:
        directory (str): The directory to search in
        extension (str): The file extension to search for (e.g., 'pdf')
        file_system (dict): The simulated file system structure
        path_prefix (str): Path prefix for constructing full file paths
        
    Returns:
        list: List of paths to files with the specified extension
        
    Base case:
        When we reach a file, check if it has the target extension
        
    Recursive case:
        When we encounter a directory, search each item inside it
    """
    # Use the sample file system if none provided
    if file_system is None:
        file_system = create_sample_file_system()
    
    # Check if file_system is a valid dictionary
    if not isinstance(file_system, dict):
        raise TypeError("File system must be a dictionary")
    
    # TODO: Implement the recursive file search logic
    # You should handle different cases such as:
    # 1. Convert the extension to a string and lowercase
    # 2. If directory is specified, navigate to that directory first
    # 3. For files, check if they end with the specified extension
    # 4. For directories, call find_by_extension recursively
    # 5. Return a list of matching file paths
    
    # Placeholder return
    return []

def find_by_name(directory, pattern, file_system=None, path_prefix=""):
    """
    Recursively find all files whose names contain a specific pattern.
    
    Args:
        directory (str): The directory to search in
        pattern (str): The name pattern to search for
        file_system (dict): The simulated file system structure
        path_prefix (str): Path prefix for constructing full file paths
        
    Returns:
        list: List of paths to files matching the name pattern
        
    Base case:
        When we reach a file, check if its name contains the pattern
        
    Recursive case:
        When we encounter a directory, search each item inside it
    """
    # Use the sample file system if none provided
    if file_system is None:
        file_system = create_sample_file_system()
    
    # Check if file_system is a valid dictionary
    if not isinstance(file_system, dict):
        raise TypeError("File system must be a dictionary")
    
    # TODO: Implement the recursive name search logic
    # You should handle different cases such as:
    # 1. Convert the pattern to a string and lowercase
    # 2. If directory is specified, navigate to that directory first
    # 3. For files, check if their name contains the pattern
    # 4. For directories, call find_by_name recursively
    # 5. Return a list of matching file paths
    
    # Placeholder return
    return []

def count_files_by_type(directory, file_system=None):
    """
    Recursively count files by their extension.
    
    Args:
        directory (str): The directory to analyze
        file_system (dict): The simulated file system structure
        
    Returns:
        dict: Dictionary with extensions as keys and counts as values
        
    Base case:
        When we reach a file, increment the count for its extension
        
    Recursive case:
        When we encounter a directory, count files in all its subdirectories
    """
    # Use the sample file system if none provided
    if file_system is None:
        file_system = create_sample_file_system()
    
    # Check if file_system is a valid dictionary
    if not isinstance(file_system, dict):
        raise TypeError("File system must be a dictionary")
    
    # TODO: Implement the recursive file counting logic
    # You should handle different cases such as:
    # 1. If directory is specified, navigate to that directory first
    # 2. For files, extract the extension and increment its count
    # 3. For directories, call count_files_by_type recursively and merge the results
    # 4. Return a dictionary with extensions as keys and counts as values
    
    # Placeholder return
    return {}

def find_largest_files(directory, n, file_system=None):
    """
    Recursively find the n largest files in a directory.
    
    Args:
        directory (str): The directory to search in
        n (int): The number of large files to find
        file_system (dict): The simulated file system structure
        
    Returns:
        list: List of tuples (path, size) for the n largest files
        
    Base case:
        When we reach a file, consider it for the largest files list
        
    Recursive case:
        When we encounter a directory, search all its subdirectories
    """
    # Validate n parameter
    try:
        n = int(n)
        if n < 0:
            return []  # Return empty list for negative n
    except (TypeError, ValueError):
        raise TypeError("n must be an integer")
    
    # Use the sample file system if none provided
    if file_system is None:
        file_system = create_sample_file_system()
    
    # Check if file_system is a valid dictionary
    if not isinstance(file_system, dict):
        raise TypeError("File system must be a dictionary")
    
    # TODO: Implement the recursive search for largest files
    # You should handle different cases such as:
    # 1. Create a helper function to collect all files with their sizes
    # 2. If directory is specified, navigate to that directory first
    # 3. Call the helper function to collect all files recursively
    # 4. Sort the files by size and return the n largest ones
    
    # Placeholder return
    return []

def format_file_size(size_bytes):
    """
    Format file size from bytes to human-readable format.
    
    Args:
        size_bytes (int): File size in bytes
        
    Returns:
        str: Human-readable file size (e.g., "1.23 MB")
    """
    try:
        size = float(size_bytes)
    except (TypeError, ValueError):
        raise TypeError("Size must be a number")
    
    # TODO: Implement the file size formatting logic
    # You should handle different units (B, KB, MB, GB, TB)
    # based on the size and return a formatted string
    
    # Placeholder return
    return "0 B"

def main():
    """
    Main function demonstrating the file system explorer.
    """
    print("===== FILE SYSTEM EXPLORER =====")
    file_system = create_sample_file_system()
    
    # Directory Summary
    print("\n----- DIRECTORY SUMMARY -----")
    # TODO: Call list_all_files and calculate_directory_size functions
    # and display the results
    
    # File Type Distribution
    print("\n----- FILE TYPE DISTRIBUTION -----")
    # TODO: Call count_files_by_type function and display the results
    
    # Search by Extension
    print("\n----- SEARCH BY EXTENSION -----")
    # TODO: Call find_by_extension function for pdf files and display the results
    
    # Search by Name
    print("\n----- SEARCH BY NAME -----")
    # TODO: Call find_by_name function for "project" files and display the results
    
    # Largest Files
    print("\n----- LARGEST FILES -----")
    # TODO: Call find_largest_files function and display the results
    
    # Specific Directory Analysis
    print("\n----- SPECIFIC DIRECTORY ANALYSIS -----")
    # TODO: Analyze the Photos directory by calling relevant functions
    # and display the results

if __name__ == "__main__":
    main()