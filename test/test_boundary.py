import pytest
from test.TestUtils import TestUtils
from file_explorer_system import (
    list_all_files,
    calculate_directory_size,
    find_by_extension,
    find_by_name,
    count_files_by_type,
    find_largest_files,
    format_file_size,
    create_sample_file_system
)

class TestBoundary:
    """Boundary tests for file system explorer functions."""
    
    def test_boundary_scenarios(self):
        """Test boundary cases for file system functions"""
        try:
            # Get the sample file system
            file_system = create_sample_file_system()
            
            # Test with empty directory
            empty_directory = {}
            empty_files = list_all_files("", empty_directory)
            assert len(empty_files) == 0, "Empty directory should return empty list"
            
            empty_size = calculate_directory_size("", empty_directory)
            assert empty_size == 0, "Empty directory should have size 0"
            
            # Test with single file system (not nested)
            single_file_system = {"file.txt": 1000}
            single_files = list_all_files("", single_file_system)
            assert len(single_files) == 1, "Single file system should return one file"
            assert single_files[0] == "file.txt", "Single file path should be correct"
            
            single_size = calculate_directory_size("", single_file_system)
            assert single_size == 1000, "Single file size should be calculated correctly"
            
            # Test with deeply nested structure
            nested_system = {
                "level1": {
                    "level2": {
                        "level3": {
                            "level4": {
                                "deep_file.txt": 100
                            }
                        }
                    }
                }
            }
            
            deep_files = list_all_files("", nested_system)
            assert len(deep_files) == 1, "Deeply nested system should find the file"
            assert "deep_file.txt" in deep_files[0], "Should find deeply nested file"
            
            deep_size = calculate_directory_size("", nested_system)
            assert deep_size == 100, "Deeply nested file size should be calculated correctly"
            
            # Test directory that doesn't exist
            nonexistent_files = list_all_files("NonExistentFolder", file_system)
            assert len(nonexistent_files) == 0, "Nonexistent directory should return empty list"
            
            nonexistent_size = calculate_directory_size("NonExistentFolder", file_system)
            assert nonexistent_size == 0, "Nonexistent directory should have size 0"
            
            # Test finding files by extension with various boundary cases
            all_pdfs = find_by_extension("", "pdf", file_system)
            assert len(all_pdfs) > 0, "Should find PDF files"
            
            no_extension_files = find_by_extension("", "xyz", file_system)
            assert len(no_extension_files) == 0, "Should return empty list for nonexistent extension"
            
            # Test case sensitivity in extension search
            pdf_upper = find_by_extension("", "PDF", file_system)
            assert len(pdf_upper) == len(all_pdfs), "Extension search should be case insensitive"
            
            # Test find by name with boundary cases
            project_files = find_by_name("", "project", file_system)
            assert len(project_files) > 0, "Should find files containing 'project'"
            
            nonexistent_name = find_by_name("", "xyznonexistent", file_system)
            assert len(nonexistent_name) == 0, "Should return empty list for nonexistent name"
            
            # Test case sensitivity in name search
            project_upper = find_by_name("", "PROJECT", file_system)
            assert len(project_upper) == len(project_files), "Name search should be case insensitive"
            
            # Test count files by type with boundary cases
            type_counts = count_files_by_type("", file_system)
            assert len(type_counts) > 0, "Should count different file types"
            assert "pdf" in type_counts, "Should count PDF files"
            
            empty_counts = count_files_by_type("", empty_directory)
            assert len(empty_counts) == 0, "Empty directory should have no file types"
            
            # Test find largest files with boundary cases
            largest_files = find_largest_files("", 5, file_system)
            assert len(largest_files) <= 5, "Should return at most 5 files"
            if len(largest_files) > 0:
                assert largest_files[0][1] >= largest_files[-1][1], "Files should be sorted by size (descending)"
            
            # Test with n larger than total files
            all_largest = find_largest_files("", 1000, file_system)
            total_files = len(list_all_files("", file_system))
            assert len(all_largest) == total_files, "Should return all files when n > total files"
            
            # Test zero files request
            zero_largest = find_largest_files("", 0, file_system)
            assert len(zero_largest) == 0, "Should return empty list when n=0"
            
            # Test format_file_size with boundary values
            assert format_file_size(0) == "0 B", "Zero bytes should format correctly"
            assert format_file_size(1023) == "1023 B", "Bytes should format correctly"
            assert "KB" in format_file_size(1024), "KB should be used for 1024+ bytes"
            assert "MB" in format_file_size(1024*1024), "MB should be used for 1MB+ bytes"
            assert "GB" in format_file_size(1024*1024*1024), "GB should be used for 1GB+ bytes"
            
            TestUtils.yakshaAssert("TestBoundaryScenarios", True, "boundary")
        except Exception as e:
            TestUtils.yakshaAssert("TestBoundaryScenarios", False, "boundary")
            pytest.fail(f"Boundary scenarios test failed: {str(e)}")


if __name__ == '__main__':
    pytest.main(['-v'])