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
    
    def test_boundary_scenarios(self):
        """Test boundary cases for file system functions"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
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
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
                return
            
            # Check for proper implementations (not just TODO/pass)
            unimplemented_functions = []
            for func_name in required_functions:
                if not check_for_implementation(self.module_obj, func_name):
                    unimplemented_functions.append(func_name)
            
            if unimplemented_functions:
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
                return
            
            # Track test results
            test_results = {}
            
            # Get the sample file system
            file_system = safely_call_function(self.module_obj, "create_sample_file_system")
            if file_system is None:
                test_results["file_system_creation"] = False
                # Create fallback file system matching solution
                file_system = {
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
            else:
                test_results["file_system_creation"] = True
            
            # Test 1: Empty directory handling
            empty_directory = {}
            empty_files = safely_call_function(self.module_obj, "list_all_files", "", empty_directory)
            test_results["empty_directory_files"] = (
                empty_files is not None and isinstance(empty_files, list) and len(empty_files) == 0
            )
            
            empty_size = safely_call_function(self.module_obj, "calculate_directory_size", "", empty_directory)
            test_results["empty_directory_size"] = (
                empty_size is not None and isinstance(empty_size, int) and empty_size == 0
            )
            
            # Test 2: Single file system
            single_file_system = {"file.txt": 1000}
            single_files = safely_call_function(self.module_obj, "list_all_files", "", single_file_system)
            test_results["single_file_listing"] = (
                single_files is not None and isinstance(single_files, list) and 
                len(single_files) == 1 and "file.txt" in single_files[0]
            )
            
            single_size = safely_call_function(self.module_obj, "calculate_directory_size", "", single_file_system)
            test_results["single_file_size"] = (
                single_size is not None and isinstance(single_size, int) and single_size == 1000
            )
            
            # Test 3: Deeply nested structure
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
            
            deep_files = safely_call_function(self.module_obj, "list_all_files", "", nested_system)
            test_results["deep_nesting"] = (
                deep_files is not None and isinstance(deep_files, list) and 
                len(deep_files) == 1 and "deep_file.txt" in deep_files[0]
            )
            
            # Test 4: Non-existent directory
            nonexistent_files = safely_call_function(self.module_obj, "list_all_files", "NonExistentFolder", file_system)
            test_results["nonexistent_directory"] = (
                nonexistent_files is not None and isinstance(nonexistent_files, list) and 
                len(nonexistent_files) == 0
            )
            
            # Test 5: Extension search boundary cases
            all_pdfs = safely_call_function(self.module_obj, "find_by_extension", "", "pdf", file_system)
            test_results["pdf_search"] = (
                all_pdfs is not None and isinstance(all_pdfs, list) and len(all_pdfs) >= 4
            )
            
            no_extension_files = safely_call_function(self.module_obj, "find_by_extension", "", "xyz", file_system)
            test_results["nonexistent_extension"] = (
                no_extension_files is not None and isinstance(no_extension_files, list) and 
                len(no_extension_files) == 0
            )
            
            # Test 6: Case sensitivity in extension search
            if all_pdfs is not None and len(all_pdfs) > 0:
                pdf_upper = safely_call_function(self.module_obj, "find_by_extension", "", "PDF", file_system)
                test_results["case_insensitive_extension"] = (
                    pdf_upper is not None and len(pdf_upper) == len(all_pdfs)
                )
            else:
                test_results["case_insensitive_extension"] = False
            
            # Test 7: Name search boundary cases
            project_files = safely_call_function(self.module_obj, "find_by_name", "", "project", file_system)
            test_results["name_search"] = (
                project_files is not None and isinstance(project_files, list) and len(project_files) >= 2
            )
            
            nonexistent_name = safely_call_function(self.module_obj, "find_by_name", "", "xyznonexistent", file_system)
            test_results["nonexistent_name"] = (
                nonexistent_name is not None and isinstance(nonexistent_name, list) and 
                len(nonexistent_name) == 0
            )
            
            # Test 8: File type counting
            type_counts = safely_call_function(self.module_obj, "count_files_by_type", "", file_system)
            test_results["type_counting"] = (
                type_counts is not None and isinstance(type_counts, dict) and 
                len(type_counts) > 0 and "pdf" in type_counts and type_counts["pdf"] == 4
            )
            
            # Test 9: Largest files functionality
            largest_files = safely_call_function(self.module_obj, "find_largest_files", "", 5, file_system)
            test_results["largest_files"] = (
                largest_files is not None and isinstance(largest_files, list) and 
                len(largest_files) <= 5 and 
                all(isinstance(item, tuple) and len(item) >= 2 for item in largest_files)
            )
            
            # Test 10: File size formatting
            format_zero = safely_call_function(self.module_obj, "format_file_size", 0)
            test_results["format_zero"] = (format_zero == "0 B")
            
            format_1024 = safely_call_function(self.module_obj, "format_file_size", 1024)
            test_results["format_kb"] = (format_1024 is not None and "KB" in format_1024)
            
            format_mb = safely_call_function(self.module_obj, "format_file_size", 1048576)
            test_results["format_mb"] = (format_mb is not None and "MB" in format_mb)
            
            # Check if all tests passed
            all_passed = all(test_results.values())
            
            if not all_passed:
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
            else:
                self.test_obj.yakshaAssert("TestBoundaryScenarios", True, "boundary")
                print("TestBoundaryScenarios = Passed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
            print("TestBoundaryScenarios = Failed")

if __name__ == '__main__':
    unittest.main()