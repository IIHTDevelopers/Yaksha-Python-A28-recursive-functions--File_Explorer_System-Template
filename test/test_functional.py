import pytest
import inspect
from test.TestUtils import TestUtils
from file_explorer_system import (
    list_all_files,
    calculate_directory_size,
    find_by_extension,
    find_by_name,
    count_files_by_type,
    find_largest_files,
    format_file_size,
    create_sample_file_system,
    main
)

class TestFunctional:
    """Test class for functional tests of the File System Explorer."""
    
    def test_implementation_requirements(self):
        """Test function existence and recursive implementation"""
        try:
            # List of required function names
            required_functions = [
                "list_all_files", "calculate_directory_size", "find_by_extension",
                "find_by_name", "count_files_by_type", "find_largest_files",
                "format_file_size", "create_sample_file_system", "main"
            ]
            
            # Get all function names from the imported module
            module_functions = [name for name, obj in globals().items() 
                               if callable(obj) and not name.startswith('__') and not name.startswith('Test')]
            
            # Check each required function exists
            for func_name in required_functions:
                assert func_name in module_functions, f"Required function '{func_name}' is missing"
            
            # Check that main recursive functions use recursion
            recursive_functions = [
                list_all_files, calculate_directory_size, find_by_extension,
                find_by_name, count_files_by_type, find_largest_files
            ]
            
            for func in recursive_functions:
                source = inspect.getsource(func)
                function_name = func.__name__
                assert function_name in source, f"Function {function_name} does not appear to be recursive"
            
            # Verify file system structure
            file_system = create_sample_file_system()
            assert "Documents" in file_system and "Downloads" in file_system, "Root directories missing"
            assert "temp.txt" in file_system, "Root-level file missing"
            assert file_system["temp.txt"] == 2000, "File size incorrect"
            assert "Projects" in file_system["Documents"], "Nested directory missing"
            assert file_system["Documents"]["Projects"]["project1.docx"] == 2500000, "Nested file size incorrect"
            
            TestUtils.yakshaAssert("TestImplementationRequirements", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("TestImplementationRequirements", False, "functional")
            pytest.fail(f"Implementation requirements test failed: {str(e)}")
    
    def test_directory_operations(self):
        """Test directory traversal and size calculation"""
        try:
            file_system = create_sample_file_system()
            
            # Test listing all files
            all_files = list_all_files("", file_system)
            assert isinstance(all_files, list) and len(all_files) > 0, "list_all_files should return a non-empty list"
            
            # Verify specific file paths are found
            report_pdf = [f for f in all_files if "report.pdf" in f]
            assert len(report_pdf) == 1, "Should find report.pdf"
            
            # Test specific directory paths
            documents_files = list_all_files("Documents", file_system)
            projects_files = list_all_files("Documents/Projects", file_system)
            photos_files = list_all_files("Documents/Personal/Photos", file_system)
            
            assert len(projects_files) == 4, "Projects directory should contain 4 files"
            assert len(photos_files) == 3, "Photos directory should contain 3 files"
            
            # Test directory sizes
            total_size = calculate_directory_size("", file_system)
            assert isinstance(total_size, int) and total_size > 0, "Root directory should have positive size"
            
            projects_size = calculate_directory_size("Documents/Projects", file_system)
            photos_size = calculate_directory_size("Documents/Personal/Photos", file_system)
            temp_size = calculate_directory_size("temp.txt", file_system)
            
            assert projects_size == 4665000, "Projects directory size incorrect"
            assert photos_size == 10500000, "Photos directory size incorrect"
            assert temp_size == 2000, "Individual file size incorrect"
            
            # Test non-existent paths
            nonexistent_files = list_all_files("NonExistentFolder", file_system)
            nonexistent_size = calculate_directory_size("NonExistentFolder", file_system)
            
            assert len(nonexistent_files) == 0, "Non-existent directory should return empty list"
            assert nonexistent_size == 0, "Non-existent directory should have zero size"
            
            TestUtils.yakshaAssert("TestDirectoryOperations", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("TestDirectoryOperations", False, "functional")
            pytest.fail(f"Directory operations test failed: {str(e)}")
    
    def test_search_and_analysis(self):
        """Test file search and analysis functions"""
        try:
            file_system = create_sample_file_system()
            
            # Test extension search
            pdf_files = find_by_extension("", "pdf", file_system)
            assert len(pdf_files) == 4, "Should find 4 PDF files"
            
            # Test case insensitivity
            PDF_files = find_by_extension("", "PDF", file_system)
            assert len(PDF_files) == len(pdf_files), "Extension search should be case-insensitive"
            
            # Test scoped searches
            docx_in_docs = find_by_extension("Documents", "docx", file_system)
            assert len(docx_in_docs) == 2, "Should find 2 DOCX files in Documents"
            
            txt_in_projects = find_by_extension("Documents/Projects", "txt", file_system)
            assert len(txt_in_projects) == 1, "Should find 1 TXT file in Projects"
            
            # Test name pattern search
            project_files = find_by_name("", "project", file_system)
            assert len(project_files) == 2, "Should find 2 files containing 'project'"
            
            # Test case insensitivity for name search
            PROJECT_files = find_by_name("", "PROJECT", file_system)
            assert len(PROJECT_files) == len(project_files), "Name search should be case-insensitive"
            
            # Test counting by file type
            type_counts = count_files_by_type("", file_system)
            assert isinstance(type_counts, dict) and len(type_counts) > 0, "Should return non-empty dict of file types"
            
            # Check specific extension counts
            assert type_counts.get("pdf") == 4, "Should find 4 PDF files"
            assert type_counts.get("docx") == 2, "Should find 2 DOCX files"
            assert type_counts.get("txt") == 2, "Should find 2 TXT files"
            
            # Test scoped type counts
            projects_counts = count_files_by_type("Documents/Projects", file_system)
            assert len(projects_counts) == 3, "Projects directory should have 3 file types"
            assert projects_counts.get("docx") == 2, "Should find 2 DOCX files in Projects"
            
            # Test finding largest files
            largest_files = find_largest_files("", 5, file_system)
            assert len(largest_files) == 5, "Should return 5 largest files"
            
            # Verify correct sorting by size
            for i in range(1, len(largest_files)):
                assert largest_files[i-1][1] >= largest_files[i][1], "Files should be sorted by size (descending)"
            
            # Verify largest file is correct
            assert largest_files[0][0] == "Downloads/video.mp4", "video.mp4 should be the largest file"
            assert largest_files[0][1] == 35000000, "video.mp4 should be 35,000,000 bytes"
            
            # Test with specific directory
            photos_largest = find_largest_files("Documents/Personal/Photos", 2, file_system)
            assert photos_largest[0][0].endswith("graduation.png"), "graduation.png should be largest in Photos"
            
            TestUtils.yakshaAssert("TestSearchAndAnalysis", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("TestSearchAndAnalysis", False, "functional")
            pytest.fail(f"Search and analysis test failed: {str(e)}")
    
    def test_formatting_and_composition(self):
        """Test formatting and function composition"""
        try:
            file_system = create_sample_file_system()
            
            # Test file size formatting
            assert format_file_size(0) == "0 B", "Zero bytes should format correctly"
            assert format_file_size(500) == "500 B", "Bytes should format correctly"
            assert format_file_size(1024) == "1.00 KB", "KB should format correctly"
            assert format_file_size(1048576) == "1.00 MB", "MB should format correctly"
            assert format_file_size(1073741824) == "1.00 GB", "GB should format correctly"
            
            # Test intermediate sizes
            assert format_file_size(2500) == "2.44 KB", "2500 bytes should format as 2.44 KB"
            assert format_file_size(1500000) == "1.43 MB", "1.5 million bytes should format as 1.43 MB"
            
            # Test function composition
            pdf_files = find_by_extension("", "pdf", file_system)
            total_pdf_size = 0
            
            for pdf_path in pdf_files:
                parts = pdf_path.split("/")
                dir_path = "/".join(parts[:-1])
                filename = parts[-1]
                
                current = file_system
                for part in dir_path.split("/"):
                    if part and part in current:
                        current = current[part]
                
                if filename in current:
                    total_pdf_size += current[filename]
            
            assert total_pdf_size == 22770000, "Total PDF size should be 22,770,000 bytes"
            
            # Test composition of search and largest functions
            largest_10 = find_largest_files("", 10, file_system)
            docx_count = sum(1 for path, _ in largest_10 if path.endswith(".docx"))
            assert docx_count in [0, 1, 2], "DOCX count in largest 10 files should be 0, 1, or 2"
            
            TestUtils.yakshaAssert("TestFormattingAndComposition", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("TestFormattingAndComposition", False, "functional")
            pytest.fail(f"Formatting and composition test failed: {str(e)}")
    
    def test_advanced_edge_cases(self):
        """Test advanced edge cases to catch subtle implementation issues"""
        try:
            file_system = create_sample_file_system()
            
            # Test for proper path joining in list_all_files
            flat_files = list_all_files("", {"file1.txt": 100, "file2.txt": 200})
            for file in flat_files:
                assert "/" not in file or file.startswith("/"), "Paths should be properly joined without double separators"
            
            # Test find_by_extension uses endswith not just contains
            doc_files = find_by_extension("", "doc", file_system)
            docx_files = find_by_extension("", "docx", file_system)
            assert len([f for f in doc_files if f.endswith(".doc")]) == len(doc_files), "Should only match exact extensions"
            # This file should be in docx but not doc results
            for docx_file in docx_files:
                if docx_file.endswith(".docx"):
                    assert docx_file not in doc_files, "Should not include .docx files when searching for .doc"
            
            # Test for accurate type count merging from subdirectories
            # Create a nested structure with duplicate extensions
            nested_fs = {
                "dir1": {"file1.txt": 100, "file2.txt": 200},
                "dir2": {"file3.txt": 300, "file4.txt": 400}
            }
            
            type_counts = count_files_by_type("", nested_fs)
            assert type_counts.get("txt") == 4, "Should count all .txt files from all subdirectories"
            
            # Test find_largest_files is truly recursive
            # Create a structure where largest files are several levels deep
            deep_fs = {
                "dir1": {"small.txt": 100},
                "dir2": {
                    "subdir": {
                        "deepfile.txt": 5000  # This should be found if truly recursive
                    }
                }
            }
            
            # Fix: Correct parameter order - n should be second parameter, file_system should be third
            largest = find_largest_files("", 1, deep_fs)
            assert len(largest) == 1, "Should find largest file"
            assert largest[0][0].endswith("deepfile.txt"), "Should find deeply nested largest file"
            
            # Test find_by_name also checks directory names
            dir_fs = {
                "project_folder": {
                    "random.txt": 100
                },
                "data": {
                    "project_data.txt": 200
                }
            }
            
            project_results = find_by_name("", "project", dir_fs, include_dirs=True)
            assert len(project_results) >= 2, "Should find files and directories with matching names"
            
            TestUtils.yakshaAssert("TestAdvancedEdgeCases", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("TestAdvancedEdgeCases", False, "functional")
            pytest.fail(f"Advanced edge cases test failed: {str(e)}")


if __name__ == '__main__':
    pytest.main(['-v'])