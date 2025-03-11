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
    all_files = []
    
    # Use the sample file system if none provided
    if file_system is None:
        file_system = create_sample_file_system()
    
    # Check if file_system is a valid dictionary
    if not isinstance(file_system, dict):
        raise TypeError("File system must be a dictionary")
    
    # Navigate to target directory if specified
    if directory:
        try:
            parts = str(directory).split("/")
            current = file_system
            for part in parts:
                if part and part in current:
                    current = current[part]
                else:
                    return []  # Directory not found
        except (TypeError, AttributeError):
            return []  # Invalid directory format
    else:
        current = file_system
    
    # Check if current is a valid dictionary to iterate
    if not isinstance(current, dict):
        return []
    
    # Process the directory content
    for name, content in current.items():
        current_path = f"{path_prefix}/{name}" if path_prefix else name
        
        if isinstance(content, dict):
            # Recursive case: it's a directory, explore it
            sub_files = list_all_files("", content, current_path)
            all_files.extend(sub_files)
        else:
            # Base case: it's a file, add it to our list
            all_files.append(current_path)
    
    return all_files

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
    total_size = 0
    
    # Use the sample file system if none provided
    if file_system is None:
        file_system = create_sample_file_system()
    
    # Check if file_system is a valid dictionary
    if not isinstance(file_system, dict):
        raise TypeError("File system must be a dictionary")
    
    # Navigate to target directory if specified
    if directory:
        try:
            parts = str(directory).split("/")
            current = file_system
            for part in parts:
                if part and part in current:
                    current = current[part]
                else:
                    return 0  # Directory not found
        except (TypeError, AttributeError):
            return 0  # Invalid directory format
    else:
        current = file_system
    
    # If it's a file, return its size
    if isinstance(current, int):
        return current
    
    # If it's not a dictionary, return 0
    if not isinstance(current, dict):
        return 0
    
    # If it's a directory, sum the sizes of all contents
    for name, content in current.items():
        if isinstance(content, dict):
            # Recursive case: it's a directory
            total_size += calculate_directory_size("", content)
        else:
            # Base case: it's a file
            total_size += content
    
    return total_size

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
    matching_files = []
    
    # Use the sample file system if none provided
    if file_system is None:
        file_system = create_sample_file_system()
    
    # Check if file_system is a valid dictionary
    if not isinstance(file_system, dict):
        raise TypeError("File system must be a dictionary")
    
    # Handle non-string extension
    try:
        extension = str(extension).lower()
    except (TypeError, AttributeError):
        return []  # Invalid extension format
    
    # Navigate to target directory if specified
    if directory:
        try:
            parts = str(directory).split("/")
            current = file_system
            for part in parts:
                if part and part in current:
                    current = current[part]
                else:
                    return []  # Directory not found
        except (TypeError, AttributeError):
            return []  # Invalid directory format
    else:
        current = file_system
    
    # Check if current is a valid dictionary to iterate
    if not isinstance(current, dict):
        return []
    
    # Process the directory content
    for name, content in current.items():
        current_path = f"{path_prefix}/{name}" if path_prefix else name
        
        if isinstance(content, dict):
            # Recursive case: it's a directory, search it
            sub_matches = find_by_extension("", extension, content, current_path)
            matching_files.extend(sub_matches)
        else:
            # Base case: it's a file, check its extension
            try:
                if str(name).lower().endswith(f".{extension}"):
                    matching_files.append(current_path)
            except (TypeError, AttributeError):
                continue  # Skip if name is not a valid string
    
    return matching_files

def find_by_name(directory, pattern, file_system=None, path_prefix="", include_dirs=False):
    matching_files = []
    
    if file_system is None:
        file_system = create_sample_file_system()

    if not isinstance(file_system, dict):
        raise TypeError("File system must be a dictionary")
    
    try:
        pattern = str(pattern).lower()
    except (TypeError, AttributeError):
        return []

    if directory:
        try:
            parts = str(directory).split("/")
            current = file_system
            for part in parts:
                if part and part in current:
                    current = current[part]
                else:
                    return []
        except (TypeError, AttributeError):
            return []
    else:
        current = file_system

    if not isinstance(current, dict):
        return []

    for name, content in current.items():
        current_path = f"{path_prefix}/{name}" if path_prefix else name
        
        if isinstance(content, dict):
            # If include_dirs is True, add matching directories
            if include_dirs and pattern in name.lower():
                matching_files.append(current_path)

            # Recursive call, ensure include_dirs is passed properly
            sub_matches = find_by_name("", pattern, content, current_path, include_dirs=include_dirs)
            matching_files.extend(sub_matches)
        else:
            # Match file names
            if pattern in name.lower():
                matching_files.append(current_path)

    return matching_files


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
    extension_counts = {}
    
    # Use the sample file system if none provided
    if file_system is None:
        file_system = create_sample_file_system()
    
    # Check if file_system is a valid dictionary
    if not isinstance(file_system, dict):
        raise TypeError("File system must be a dictionary")
    
    # Navigate to target directory if specified
    if directory:
        try:
            parts = str(directory).split("/")
            current = file_system
            for part in parts:
                if part and part in current:
                    current = current[part]
                else:
                    return {}  # Directory not found
        except (TypeError, AttributeError):
            return {}  # Invalid directory format
    else:
        current = file_system
    
    # If it's a file, return an empty dictionary
    if isinstance(current, int):
        return {}
    
    # If it's not a dictionary, return an empty dictionary
    if not isinstance(current, dict):
        return {}
    
    # Process the directory content
    for name, content in current.items():
        if isinstance(content, dict):
            # Recursive case: it's a directory
            sub_counts = count_files_by_type("", content)
            # Merge the counts
            for ext, count in sub_counts.items():
                extension_counts[ext] = extension_counts.get(ext, 0) + count
        else:
            # Base case: it's a file, get its extension
            try:
                parts = str(name).split(".")
                if len(parts) > 1:
                    ext = parts[-1].lower()
                    extension_counts[ext] = extension_counts.get(ext, 0) + 1
                else:
                    # File has no extension
                    extension_counts["no_extension"] = extension_counts.get("no_extension", 0) + 1
            except (TypeError, AttributeError):
                # Handle non-string file names
                extension_counts["unknown"] = extension_counts.get("unknown", 0) + 1
    
    return extension_counts

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
    # List to store (path, size) tuples
    largest_files = []
    
    # Validate n parameter
    try:
        n = int(n)
        if n < 0:
            return []  # Return empty list for negative n
    except (TypeError, ValueError):
        raise TypeError("n must be an integer")
    
    def collect_files(current, path_prefix=""):
        """Helper function to collect files with their sizes"""
        if not isinstance(current, dict):
            return
            
        for name, content in current.items():
            try:
                current_path = f"{path_prefix}/{name}" if path_prefix else name
                
                if isinstance(content, dict):
                    # Recursive case: it's a directory
                    collect_files(content, current_path)
                else:
                    # Base case: it's a file
                    largest_files.append((current_path, content))
            except (TypeError, AttributeError):
                continue  # Skip if there's an error with this item
    
    # Use the sample file system if none provided
    if file_system is None:
        file_system = create_sample_file_system()
    
    # Check if file_system is a valid dictionary
    if not isinstance(file_system, dict):
        raise TypeError("File system must be a dictionary")
    
    # Navigate to target directory if specified
    if directory:
        try:
            parts = str(directory).split("/")
            current = file_system
            for part in parts:
                if part and part in current:
                    current = current[part]
                else:
                    return []  # Directory not found
        except (TypeError, AttributeError):
            return []  # Invalid directory format
    else:
        current = file_system
    
    # Collect all files
    if isinstance(current, int):
        return []  # It's a file, not a directory
    
    if not isinstance(current, dict):
        return []  # It's not a valid directory
    
    collect_files(current)
    
    # Sort by size (descending) and return top n
    largest_files.sort(key=lambda x: x[1], reverse=True)
    return largest_files[:n]

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
        if size < 0:
            size = abs(size)  # Handle negative sizes gracefully
            
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024 or unit == 'TB':
                if unit == 'B':
                    return f"{int(size)} {unit}"
                return f"{size:.2f} {unit}"
            size /= 1024
    except (TypeError, ValueError):
        raise TypeError("Size must be a number")

def main():
    """
    Main function demonstrating the file system explorer.
    """
    print("===== FILE SYSTEM EXPLORER =====")
    file_system = create_sample_file_system()
    
    # Directory Summary
    print("\n----- DIRECTORY SUMMARY -----")
    all_files = list_all_files("", file_system)
    total_size = calculate_directory_size("", file_system)
    print(f"Total files: {len(all_files)}")
    print(f"Total size: {format_file_size(total_size)}")
    
    # File Type Distribution
    print("\n----- FILE TYPE DISTRIBUTION -----")
    type_counts = count_files_by_type("", file_system)
    for ext, count in sorted(type_counts.items()):
        print(f"{ext}: {count} files")
    
    # Search by Extension
    print("\n----- SEARCH BY EXTENSION -----")
    pdf_files = find_by_extension("", "pdf", file_system)
    print("PDF files:")
    for file in pdf_files:
        print(f"  {file}")
    
    # Search by Name
    print("\n----- SEARCH BY NAME -----")
    project_files = find_by_name("", "project", file_system)
    print("Files containing 'project':")
    for file in project_files:
        print(f"  {file}")
        
    # Search by Name including directories
    print("\n----- SEARCH BY NAME (INCLUDING DIRECTORIES) -----")
    project_all = find_by_name("", "project", file_system, include_dirs=True)
    print("Files and directories containing 'project':")
    for item in project_all:
        print(f"  {item}")
    
    # Largest Files
    print("\n----- LARGEST FILES -----")
    largest = find_largest_files("", 5, file_system)
    print("Top 5 largest files:")
    for path, size in largest:
        print(f"  {path} ({format_file_size(size)})")
    
    # Specific Directory Analysis
    print("\n----- SPECIFIC DIRECTORY ANALYSIS -----")
    photos_size = calculate_directory_size("Documents/Personal/Photos", file_system)
    photos_files = list_all_files("Documents/Personal/Photos", file_system)
    print(f"Photos directory size: {format_file_size(photos_size)}")
    print(f"Photos directory files: {len(photos_files)}")
    for file in photos_files:
        print(f"  {file}")

if __name__ == "__main__":
    main()