import unittest
import os
import importlib
import sys
import io
import contextlib
import inspect
from test.TestUtils import TestUtils

def safely_import_module(module_name):
    """Safely import a module, returning None if import fails."""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None

def check_function_exists(module, function_name):
    """Check if a function exists in a module."""
    return hasattr(module, function_name) and callable(getattr(module, function_name))

def safely_call_function(module, function_name, *args, **kwargs):
    """Safely call a function, returning None if it fails."""
    if not check_function_exists(module, function_name):
        return None
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return getattr(module, function_name)(*args, **kwargs)
    except Exception:
        return None

def check_exception_raised(module, function_name, expected_exceptions, *args, **kwargs):
    """Check if a function raises the expected exception."""
    if not check_function_exists(module, function_name):
        return False
    
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            getattr(module, function_name)(*args, **kwargs)
        return False  # No exception raised
    except Exception as e:
        # Check if the exception is one of the expected types
        return any(isinstance(e, exc) for exc in expected_exceptions)

def check_for_implementation(module, function_name):
    """Check if a function has a real implementation and not just 'pass'."""
    if not check_function_exists(module, function_name):
        return False
    try:
        source = inspect.getsource(getattr(module, function_name))
        # Check for actual implementation - look for meaningful code beyond just 'pass'
        lines = [line.strip() for line in source.split('\n') if line.strip()]
        non_trivial_lines = [line for line in lines if not line.startswith('#') and 
                           line not in ['pass', f'def {function_name}'] and
                           not line.startswith('"""') and not line.startswith("'''") and
                           'return []' not in line and 'return 0' not in line and 
                           'return {}' not in line and 'return "0 B"' not in line]
        return len(non_trivial_lines) > 3  # Function must have more than basic structure
    except Exception:
        return False

def load_module_dynamically():
    """Load the student's module for testing"""
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    return module_obj

class TestAssignment(unittest.TestCase):
    def setUp(self):
        """Standard setup for all test methods"""
        self.test_obj = TestUtils()
        self.module_obj = load_module_dynamically()
    
    def test_exceptional_cases(self):
        """Test error handling and invalid inputs across all functions"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestExceptionalCases", False, "exception")
                print("TestExceptionalCases = Failed")
                return
            
            # Check required functions exist
            required_functions = [
                "list_all_files",
                "calculate_directory_size",
                "find_by_extension", 
                "find_by_name",
                "count_files_by_type",
                "find_largest_files",
                "format_file_size",
                "create_sample_file_system"
            ]
            
            missing_functions = []
            for func_name in required_functions:
                if not check_function_exists(self.module_obj, func_name):
                    missing_functions.append(func_name)
            
            if missing_functions:
                self.test_obj.yakshaAssert("TestExceptionalCases", False, "exception")
                print("TestExceptionalCases = Failed")
                return
            
            # Check for proper implementations (not just TODO/pass)
            unimplemented_functions = []
            for func_name in required_functions:
                if not check_for_implementation(self.module_obj, func_name):
                    unimplemented_functions.append(func_name)
            
            if unimplemented_functions:
                self.test_obj.yakshaAssert("TestExceptionalCases", False, "exception")
                print("TestExceptionalCases = Failed")
                return
            
            # Track test results
            test_results = {}
            
            # Get sample file system
            file_system = safely_call_function(self.module_obj, "create_sample_file_system")
            if file_system is None:
                test_results["file_system_creation"] = False
                # Create fallback file system
                file_system = {
                    "Documents": {
                        "Projects": {
                            "project1.docx": 2500000,
                            "project2.docx": 1800000,
                            "notes.txt": 15000,
                            "data.csv": 350000,
                        }
                    },
                    "temp.txt": 2000
                }
            else:
                test_results["file_system_creation"] = True
            
            # Test 1: Invalid file system input (string instead of dict)
            invalid_fs = "not a dictionary"
            
            test_functions = [
                ("list_all_files", ("",)),
                ("calculate_directory_size", ("",)),
                ("find_by_extension", ("", "pdf")),
                ("find_by_name", ("", "test")),
                ("count_files_by_type", ("",))
            ]
            
            invalid_fs_tests_passed = 0
            for func_name, args in test_functions:
                # Test with invalid file system
                exception_raised = check_exception_raised(
                    self.module_obj,
                    func_name,
                    (TypeError, AttributeError),
                    *args,
                    invalid_fs  # Pass as positional argument
                )
                
                if exception_raised:
                    invalid_fs_tests_passed += 1
                else:
                    # Check for graceful handling
                    result = safely_call_function(self.module_obj, func_name, *args, invalid_fs)
                    if result is not None and isinstance(result, (list, dict, int)):
                        invalid_fs_tests_passed += 1  # Graceful handling acceptable
            
            test_results["invalid_file_system"] = (invalid_fs_tests_passed >= 3)
            
            # Test 2: Non-string directory path
            non_string_path_tests = 0
            
            exception_raised = check_exception_raised(
                self.module_obj,
                "list_all_files",
                (TypeError, ValueError, AttributeError),
                123,
                file_system
            )
            if exception_raised:
                non_string_path_tests += 1
            else:
                result = safely_call_function(self.module_obj, "list_all_files", 123, file_system)
                if result is not None and isinstance(result, list):
                    non_string_path_tests += 1  # Graceful handling
            
            test_results["non_string_path"] = (non_string_path_tests > 0)
            
            # Test 3: Non-string extension
            non_string_ext_tests = 0
            
            exception_raised = check_exception_raised(
                self.module_obj,
                "find_by_extension",
                (TypeError, ValueError, AttributeError),
                "",
                123,
                file_system
            )
            if exception_raised:
                non_string_ext_tests += 1
            else:
                result = safely_call_function(self.module_obj, "find_by_extension", "", 123, file_system)
                if result is not None and isinstance(result, list):
                    non_string_ext_tests += 1  # Graceful handling
            
            test_results["non_string_extension"] = (non_string_ext_tests > 0)
            
            # Test 4: Non-string pattern
            non_string_pattern_tests = 0
            
            exception_raised = check_exception_raised(
                self.module_obj,
                "find_by_name",
                (TypeError, ValueError, AttributeError),
                "",
                123,
                file_system
            )
            if exception_raised:
                non_string_pattern_tests += 1
            else:
                result = safely_call_function(self.module_obj, "find_by_name", "", 123, file_system)
                if result is not None and isinstance(result, list):
                    non_string_pattern_tests += 1  # Graceful handling
            
            test_results["non_string_pattern"] = (non_string_pattern_tests > 0)
            
            # Test 5: Non-integer n in find_largest_files
            non_int_n_exception = check_exception_raised(
                self.module_obj,
                "find_largest_files",
                (TypeError, ValueError),
                "",
                "not a number",
                file_system
            )
            test_results["non_integer_n"] = non_int_n_exception
            
            # Test 6: Non-numeric size in format_file_size
            non_numeric_size_exception = check_exception_raised(
                self.module_obj,
                "format_file_size",
                (TypeError, ValueError),
                "not a number"
            )
            test_results["non_numeric_size"] = non_numeric_size_exception
            
            # Test 7: Negative values handling
            negative_n = safely_call_function(self.module_obj, "find_largest_files", "", -5, file_system)
            test_results["negative_n"] = (
                negative_n is not None and isinstance(negative_n, list) and len(negative_n) == 0
            )
            
            negative_size = safely_call_function(self.module_obj, "format_file_size", -1024)
            test_results["negative_size"] = (negative_size is not None and isinstance(negative_size, str))
            
            # Test 8: Unusual file system structures
            unusual_structures = [
                {"file1.txt": {"subfile.txt": 100}},  # File treated as directory
                {123: 100}  # Number as filename
            ]
            
            unusual_structure_tests = 0
            for structure in unusual_structures:
                # These should not crash
                result1 = safely_call_function(self.module_obj, "list_all_files", "", structure)
                result2 = safely_call_function(self.module_obj, "calculate_directory_size", "", structure)
                result3 = safely_call_function(self.module_obj, "find_by_extension", "", "txt", structure)
                
                if all(r is not None for r in [result1, result2, result3]):
                    unusual_structure_tests += 1
                else:
                    unusual_structure_tests += 0.5  # Partial credit for not crashing
            
            test_results["unusual_structures"] = (unusual_structure_tests >= 1)
            
            # Test 9: Empty string inputs
            empty_string_tests = 0
            
            empty_dir_result = safely_call_function(self.module_obj, "list_all_files", "", file_system)
            if empty_dir_result is not None and isinstance(empty_dir_result, list):
                empty_string_tests += 1
            
            dot_dir_result = safely_call_function(self.module_obj, "list_all_files", ".", file_system)
            if dot_dir_result is not None and isinstance(dot_dir_result, list):
                empty_string_tests += 1
            
            test_results["empty_string_inputs"] = (empty_string_tests >= 1)
            
            # Test 10: Path format handling
            path_format_tests = 0
            
            slash_paths = safely_call_function(self.module_obj, "list_all_files", "/Documents/", file_system)
            if slash_paths is not None and isinstance(slash_paths, list):
                path_format_tests += 1
            
            double_slash = safely_call_function(self.module_obj, "list_all_files", "Documents//Personal", file_system)
            if double_slash is not None and isinstance(double_slash, list):
                path_format_tests += 1
            
            test_results["path_formats"] = (path_format_tests >= 1)
            
            # Test 11: Extreme values
            huge_n = safely_call_function(self.module_obj, "find_largest_files", "", 1000000, file_system)
            test_results["huge_n"] = (huge_n is not None and isinstance(huge_n, list))
            
            huge_size_format = safely_call_function(self.module_obj, "format_file_size", 10**20)
            test_results["huge_size"] = (huge_size_format is not None and isinstance(huge_size_format, str))
            
            # Check if most tests passed (allow some flexibility for different implementations)
            passed_tests = sum(1 for result in test_results.values() if result)
            total_tests = len(test_results)
            success_rate = passed_tests / total_tests
            
            if success_rate >= 0.7:  # 70% pass rate acceptable for exception handling
                self.test_obj.yakshaAssert("TestExceptionalCases", True, "exception")
                print("TestExceptionalCases = Passed")
            else:
                self.test_obj.yakshaAssert("TestExceptionalCases", False, "exception")
                print("TestExceptionalCases = Failed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestExceptionalCases", False, "exception")
            print("TestExceptionalCases = Failed")

if __name__ == '__main__':
    unittest.main()