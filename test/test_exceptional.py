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

class TestExceptional:
    """Exception handling tests for file system explorer functions."""
    
    def test_exceptional_cases(self):
        """Test error handling and invalid inputs across all functions"""
        try:
            # Get the sample file system
            file_system = create_sample_file_system()
            
            # ------------ PART 1: Basic Error Handling ------------
            
            # Test invalid file system input
            invalid_fs = "not a dictionary"
            
            for func_name, func, args in [
                ("list_all_files", list_all_files, ("",)),
                ("calculate_directory_size", calculate_directory_size, ("",)),
                ("find_by_extension", find_by_extension, ("", "pdf")),
                ("find_by_name", find_by_name, ("", "test")),
                ("count_files_by_type", count_files_by_type, ("",)),
                ("find_largest_files", find_largest_files, ("", 5))
            ]:
                try:
                    func(*args, file_system=invalid_fs)
                    assert False, f"{func_name} should handle non-dict file system"
                except (TypeError, AttributeError):
                    pass  # Expected exception
            
            # Test invalid input parameters
            try:
                result = list_all_files(123, file_system)  # Non-string path
                assert isinstance(result, list), "Should handle non-string directory path"
            except (TypeError, ValueError):
                pass  # Exception is acceptable
            
            try:
                result = find_by_extension("", 123, file_system)  # Non-string extension
                assert isinstance(result, list), "Should handle non-string extension"
            except (TypeError, ValueError, AttributeError):
                pass  # Exception is acceptable
            
            try:
                result = find_by_name("", 123, file_system)  # Non-string pattern
                assert isinstance(result, list), "Should handle non-string pattern"
            except (TypeError, ValueError, AttributeError):
                pass  # Exception is acceptable
            
            try:
                result = find_largest_files("", "not a number", file_system)
                assert False, "Should handle non-integer n"
            except (TypeError, ValueError):
                pass  # Expected exception
            
            try:
                format_file_size("not a number")
                assert False, "Should handle non-numeric size"
            except (TypeError, ValueError):
                pass  # Expected exception
            
            # Test with None values
            for func_name, func in [
                ("list_all_files", list_all_files),
                ("calculate_directory_size", calculate_directory_size)
            ]:
                try:
                    func(None, file_system)
                    # Should either handle gracefully or throw an exception
                except (TypeError, ValueError):
                    pass  # Exception is acceptable
            
            # ------------ PART 2: Advanced Error Cases ------------
            
            # Test negative values
            try:
                result = find_largest_files("", -5, file_system)
                # Should either handle gracefully or throw an exception
                if isinstance(result, list):
                    assert len(result) == 0, "Negative n should return empty list"
            except ValueError:
                pass  # Exception is acceptable
            
            try:
                result = format_file_size(-1024)
                # Should either handle gracefully or throw an exception
                if isinstance(result, str):
                    pass  # Handled gracefully
            except ValueError:
                pass  # Exception is acceptable
            
            # Test with unusual file system structures
            unusual_structures = [
                {"file1.txt": {"subfile.txt": 100}},  # File treated as directory
                {123: 100}  # Number as filename
            ]
            
            for structure in unusual_structures:
                try:
                    list_all_files("", structure)
                    calculate_directory_size("", structure)
                    find_by_extension("", "txt", structure)
                except Exception:
                    pass  # Exception is acceptable
            
            # Test circular references
            try:
                circular = {"folder1": {}}
                circular["folder1"]["self_ref"] = circular
                
                # These might cause recursion errors but should be handled
                list_all_files("", circular)
                calculate_directory_size("", circular)
            except (RecursionError, RuntimeError, OverflowError):
                pass  # Expected exception for circular structure
            
            # ------------ PART 3: Path Format Handling ------------
            
            # Test with unusual but valid inputs
            empty_string_dir = list_all_files("", file_system)
            assert isinstance(empty_string_dir, list), "Empty string directory should be handled"
            
            dot_dir = list_all_files(".", file_system)
            assert isinstance(dot_dir, list), "Dot directory should be handled"
            
            # Test with unusual path formats
            slash_paths = list_all_files("/Documents/", file_system)  # Leading/trailing slashes
            assert isinstance(slash_paths, list), "Paths with extra slashes should be handled"
            
            double_slash = list_all_files("Documents//Personal", file_system)  # Double slashes
            assert isinstance(double_slash, list), "Paths with double slashes should be handled"
            
            # ------------ PART 4: Extreme Values ------------
            
            # Test with extremely large values
            try:
                huge_n = find_largest_files("", 1000000, file_system)
                assert isinstance(huge_n, list), "Very large n should be handled"
            except (MemoryError, OverflowError):
                pass  # Exception is acceptable for extreme values
            
            # Test with unusual file sizes
            unusual_sizes = {
                "zero.txt": 0,
                "negative.txt": -100,  # Should be handled gracefully
                "huge.txt": 10**20,  # Very large number
            }
            
            try:
                calculate_directory_size("", unusual_sizes)
                format_file_size(unusual_sizes["huge.txt"])
            except (OverflowError, ValueError):
                pass  # Exception is acceptable for extreme values
            
            TestUtils.yakshaAssert("TestExceptionalCases", True, "exception")
        except Exception as e:
            TestUtils.yakshaAssert("TestExceptionalCases", False, "exception")
            pytest.fail(f"Exception testing failed: {str(e)}")


if __name__ == '__main__':
    pytest.main(['-v'])