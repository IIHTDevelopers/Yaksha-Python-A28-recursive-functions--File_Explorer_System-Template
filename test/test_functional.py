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
    
    def test_implementation_requirements(self):
        """Test function existence and recursive implementation"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestImplementationRequirements", False, "functional")
                print("TestImplementationRequirements = Failed")
                return
            
            # List of required function names
            required_functions = [
                "list_all_files", "calculate_directory_size", "find_by_extension",
                "find_by_name", "count_files_by_type", "find_largest_files",
                "format_file_size", "create_sample_file_system", "main"
            ]
            
            # Check each required function exists
            missing_functions = []
            for func_name in required_functions:
                if not check_function_exists(self.module_obj, func_name):
                    missing_functions.append(func_name)
            
            if missing_functions:
                self.test_obj.yakshaAssert("TestImplementationRequirements", False, "functional")
                print("TestImplementationRequirements = Failed")
                return
            
            # Check for proper implementations (not just TODO/pass)
            unimplemented_functions = []
            for func_name in required_functions:
                if not check_for_implementation(self.module_obj, func_name):
                    unimplemented_functions.append(func_name)
            
            if unimplemented_functions:
                self.test_obj.yakshaAssert("TestImplementationRequirements", False, "functional")
                print("TestImplementationRequirements = Failed")
                return
            
            # Track test results
            test_results = {}
            
            # Check that main recursive functions use recursion
            recursive_functions = [
                ("list_all_files", self.module_obj.list_all_files),
                ("calculate_directory_size", self.module_obj.calculate_directory_size),
                ("find_by_extension", self.module_obj.find_by_extension),
                ("find_by_name", self.module_obj.find_by_name),
                ("count_files_by_type", self.module_obj.count_files_by_type),
                ("find_largest_files", self.module_obj.find_largest_files)
            ]
            
            recursion_check_passed = 0
            for func_name, func in recursive_functions:
                if func is not None:
                    try:
                        source = inspect.getsource(func)
                        if func_name in source:  # Function calls itself
                            recursion_check_passed += 1
                    except Exception:
                        pass
            
            test_results["recursion_implementation"] = (recursion_check_passed >= 4)
            
            # Verify file system structure
            file_system = safely_call_function(self.module_obj, "create_sample_file_system")
            if file_system is None:
                test_results["file_system_creation"] = False
            else:
                # Check for expected structure
                expected_checks = [
                    ("Documents" in file_system, "Root directory 'Documents' missing"),
                    ("Downloads" in file_system, "Root directory 'Downloads' missing"),
                    ("temp.txt" in file_system, "Root-level file 'temp.txt' missing"),
                    (file_system.get("temp.txt") == 2000, "File 'temp.txt' has incorrect size"),
                ]
                
                structure_valid = all(check for check, _ in expected_checks)
                
                # Check nested structure if Documents exists
                if "Documents" in file_system and isinstance(file_system["Documents"], dict):
                    if "Projects" in file_system["Documents"]:
                        projects = file_system["Documents"]["Projects"]
                        if isinstance(projects, dict):
                            structure_valid = structure_valid and "project1.docx" in projects
                            structure_valid = structure_valid and projects.get("project1.docx") == 2500000
                
                test_results["file_system_creation"] = structure_valid
            
            # Check if all tests passed
            all_passed = all(test_results.values())
            
            if not all_passed:
                self.test_obj.yakshaAssert("TestImplementationRequirements", False, "functional")
                print("TestImplementationRequirements = Failed")
            else:
                self.test_obj.yakshaAssert("TestImplementationRequirements", True, "functional")
                print("TestImplementationRequirements = Passed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestImplementationRequirements", False, "functional")
            print("TestImplementationRequirements = Failed")
    
    def test_directory_operations(self):
        """Test directory traversal and size calculation"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestDirectoryOperations", False, "functional")
                print("TestDirectoryOperations = Failed")
                return
            
            # Check required functions
            required_functions = [
                "list_all_files",
                "calculate_directory_size",
                "create_sample_file_system"
            ]
            
            missing_functions = []
            for func_name in required_functions:
                if not check_function_exists(self.module_obj, func_name):
                    missing_functions.append(func_name)
            
            if missing_functions:
                self.test_obj.yakshaAssert("TestDirectoryOperations", False, "functional")
                print("TestDirectoryOperations = Failed")
                return
            
            # Check for proper implementations
            unimplemented_functions = []
            for func_name in required_functions:
                if not check_for_implementation(self.module_obj, func_name):
                    unimplemented_functions.append(func_name)
            
            if unimplemented_functions:
                self.test_obj.yakshaAssert("TestDirectoryOperations", False, "functional")
                print("TestDirectoryOperations = Failed")
                return
            
            # Track test results
            test_results = {}
            
            file_system = safely_call_function(self.module_obj, "create_sample_file_system")
            if file_system is None:
                test_results["file_system_available"] = False
                # Create fallback file system
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
                test_results["file_system_available"] = True
            
            # Test listing all files
            all_files = safely_call_function(self.module_obj, "list_all_files", "", file_system)
            test_results["list_all_files"] = (
                all_files is not None and isinstance(all_files, list) and len(all_files) > 0
            )
            
            # Verify specific file paths are found
            if all_files:
                report_pdf = [f for f in all_files if "report.pdf" in f]
                test_results["specific_file_found"] = (len(report_pdf) == 1)
            else:
                test_results["specific_file_found"] = False
            
            # Test specific directory paths
            documents_files = safely_call_function(self.module_obj, "list_all_files", "Documents", file_system)
            test_results["documents_listing"] = (
                documents_files is not None and isinstance(documents_files, list)
            )
            
            projects_files = safely_call_function(self.module_obj, "list_all_files", "Documents/Projects", file_system)
            test_results["projects_listing"] = (
                projects_files is not None and isinstance(projects_files, list) and len(projects_files) == 4
            )
            
            photos_files = safely_call_function(self.module_obj, "list_all_files", "Documents/Personal/Photos", file_system)
            test_results["photos_listing"] = (
                photos_files is not None and isinstance(photos_files, list) and len(photos_files) == 3
            )
            
            # Test directory sizes
            total_size = safely_call_function(self.module_obj, "calculate_directory_size", "", file_system)
            test_results["total_size_calculation"] = (
                total_size is not None and isinstance(total_size, int) and total_size > 0
            )
            
            projects_size = safely_call_function(self.module_obj, "calculate_directory_size", "Documents/Projects", file_system)
            expected_projects_size = 2500000 + 1800000 + 15000 + 350000  # 4665000
            test_results["projects_size"] = (
                projects_size is not None and isinstance(projects_size, int) and projects_size == expected_projects_size
            )
            
            photos_size = safely_call_function(self.module_obj, "calculate_directory_size", "Documents/Personal/Photos", file_system)
            expected_photos_size = 3500000 + 2800000 + 4200000  # 10500000
            test_results["photos_size"] = (
                photos_size is not None and isinstance(photos_size, int) and photos_size == expected_photos_size
            )
            
            # Test non-existent paths
            nonexistent_files = safely_call_function(self.module_obj, "list_all_files", "NonExistentFolder", file_system)
            test_results["nonexistent_path"] = (
                nonexistent_files is not None and isinstance(nonexistent_files, list) and len(nonexistent_files) == 0
            )
            
            nonexistent_size = safely_call_function(self.module_obj, "calculate_directory_size", "NonExistentFolder", file_system)
            test_results["nonexistent_size"] = (
                nonexistent_size is not None and isinstance(nonexistent_size, int) and nonexistent_size == 0
            )
            
            # Check if all tests passed
            all_passed = all(test_results.values())
            
            if not all_passed:
                self.test_obj.yakshaAssert("TestDirectoryOperations", False, "functional")
                print("TestDirectoryOperations = Failed")
            else:
                self.test_obj.yakshaAssert("TestDirectoryOperations", True, "functional")
                print("TestDirectoryOperations = Passed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestDirectoryOperations", False, "functional")
            print("TestDirectoryOperations = Failed")
    
    def test_search_and_analysis(self):
        """Test file search and analysis functions"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestSearchAndAnalysis", False, "functional")
                print("TestSearchAndAnalysis = Failed")
                return
            
            # Check required functions
            required_functions = [
                "find_by_extension",
                "find_by_name",
                "count_files_by_type",
                "find_largest_files",
                "create_sample_file_system"
            ]
            
            missing_functions = []
            for func_name in required_functions:
                if not check_function_exists(self.module_obj, func_name):
                    missing_functions.append(func_name)
            
            if missing_functions:
                self.test_obj.yakshaAssert("TestSearchAndAnalysis", False, "functional")
                print("TestSearchAndAnalysis = Failed")
                return
            
            # Check for proper implementations
            unimplemented_functions = []
            for func_name in required_functions:
                if not check_for_implementation(self.module_obj, func_name):
                    unimplemented_functions.append(func_name)
            
            if unimplemented_functions:
                self.test_obj.yakshaAssert("TestSearchAndAnalysis", False, "functional")
                print("TestSearchAndAnalysis = Failed")
                return
            
            # Track test results
            test_results = {}
            
            file_system = safely_call_function(self.module_obj, "create_sample_file_system")
            if file_system is None:
                test_results["file_system_available"] = False
                # Create fallback file system
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
                test_results["file_system_available"] = True
            
            # Test extension search - should find 4 PDF files
            pdf_files = safely_call_function(self.module_obj, "find_by_extension", "", "pdf", file_system)
            test_results["pdf_search"] = (
                pdf_files is not None and isinstance(pdf_files, list) and len(pdf_files) == 4
            )
            
            # Test case insensitivity
            PDF_files = safely_call_function(self.module_obj, "find_by_extension", "", "PDF", file_system)
            test_results["case_insensitive_extension"] = (
                PDF_files is not None and isinstance(PDF_files, list) and 
                pdf_files is not None and len(PDF_files) == len(pdf_files)
            )
            
            # Test scoped searches
            docx_in_docs = safely_call_function(self.module_obj, "find_by_extension", "Documents", "docx", file_system)
            test_results["scoped_docx_search"] = (
                docx_in_docs is not None and isinstance(docx_in_docs, list) and len(docx_in_docs) == 2
            )
            
            txt_in_projects = safely_call_function(self.module_obj, "find_by_extension", "Documents/Projects", "txt", file_system)
            test_results["scoped_txt_search"] = (
                txt_in_projects is not None and isinstance(txt_in_projects, list) and len(txt_in_projects) == 1
            )
            
            # Test name pattern search
            project_files = safely_call_function(self.module_obj, "find_by_name", "", "project", file_system)
            test_results["name_search"] = (
                project_files is not None and isinstance(project_files, list) and len(project_files) == 2
            )
            
            # Test case insensitivity for name search
            PROJECT_files = safely_call_function(self.module_obj, "find_by_name", "", "PROJECT", file_system)
            test_results["case_insensitive_name"] = (
                PROJECT_files is not None and isinstance(PROJECT_files, list) and 
                project_files is not None and len(PROJECT_files) == len(project_files)
            )
            
            # Test counting by file type
            type_counts = safely_call_function(self.module_obj, "count_files_by_type", "", file_system)
            test_results["type_counting"] = (
                type_counts is not None and isinstance(type_counts, dict) and len(type_counts) > 0
            )
            
            # Check specific extension counts
            if type_counts:
                test_results["pdf_count"] = (type_counts.get("pdf") == 4)
                test_results["docx_count"] = (type_counts.get("docx") == 2)
                test_results["txt_count"] = (type_counts.get("txt") == 2)  # notes.txt, temp.txt
            else:
                test_results["pdf_count"] = False
                test_results["docx_count"] = False
                test_results["txt_count"] = False
            
            # Test scoped type counts
            projects_counts = safely_call_function(self.module_obj, "count_files_by_type", "Documents/Projects", file_system)
            test_results["scoped_type_count"] = (
                projects_counts is not None and isinstance(projects_counts, dict) and 
                len(projects_counts) == 3 and projects_counts.get("docx") == 2
            )
            
            # Test finding largest files
            largest_files = safely_call_function(self.module_obj, "find_largest_files", "", 5, file_system)
            test_results["largest_files"] = (
                largest_files is not None and isinstance(largest_files, list) and len(largest_files) == 5
            )
            
            # Verify correct sorting by size
            if largest_files and len(largest_files) > 1:
                sorted_correctly = True
                for i in range(1, len(largest_files)):
                    if (isinstance(largest_files[i-1], tuple) and isinstance(largest_files[i], tuple) and
                        len(largest_files[i-1]) >= 2 and len(largest_files[i]) >= 2):
                        if largest_files[i-1][1] < largest_files[i][1]:
                            sorted_correctly = False
                            break
                test_results["largest_files_sorted"] = sorted_correctly
            else:
                test_results["largest_files_sorted"] = False
            
            # Verify largest file is correct - should be video.mp4 with 35000000 bytes
            if (largest_files and len(largest_files) > 0 and isinstance(largest_files[0], tuple) and 
                len(largest_files[0]) >= 2):
                test_results["largest_file_correct"] = (
                    "video.mp4" in largest_files[0][0] and largest_files[0][1] == 35000000
                )
            else:
                test_results["largest_file_correct"] = False
            
            # Test with specific directory
            photos_largest = safely_call_function(self.module_obj, "find_largest_files", "Documents/Personal/Photos", 2, file_system)
            test_results["scoped_largest"] = (
                photos_largest is not None and isinstance(photos_largest, list) and len(photos_largest) == 2
            )
            
            if (photos_largest and len(photos_largest) > 0 and isinstance(photos_largest[0], tuple)):
                test_results["scoped_largest_correct"] = ("graduation.png" in photos_largest[0][0])
            else:
                test_results["scoped_largest_correct"] = False
            
            # Check if most tests passed (allow some flexibility)
            passed_tests = sum(1 for result in test_results.values() if result)
            total_tests = len(test_results)
            success_rate = passed_tests / total_tests
            
            if success_rate >= 0.8:  # 80% pass rate
                self.test_obj.yakshaAssert("TestSearchAndAnalysis", True, "functional")
                print("TestSearchAndAnalysis = Passed")
            else:
                self.test_obj.yakshaAssert("TestSearchAndAnalysis", False, "functional")
                print("TestSearchAndAnalysis = Failed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestSearchAndAnalysis", False, "functional")
            print("TestSearchAndAnalysis = Failed")
    
    def test_formatting_and_composition(self):
        """Test formatting and function composition"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestFormattingAndComposition", False, "functional")
                print("TestFormattingAndComposition = Failed")
                return
            
            # Check required functions
            required_functions = [
                "format_file_size",
                "find_by_extension",
                "find_largest_files",
                "create_sample_file_system"
            ]
            
            missing_functions = []
            for func_name in required_functions:
                if not check_function_exists(self.module_obj, func_name):
                    missing_functions.append(func_name)
            
            if missing_functions:
                self.test_obj.yakshaAssert("TestFormattingAndComposition", False, "functional")
                print("TestFormattingAndComposition = Failed")
                return
            
            # Check for proper implementations
            unimplemented_functions = []
            for func_name in required_functions:
                if not check_for_implementation(self.module_obj, func_name):
                    unimplemented_functions.append(func_name)
            
            if unimplemented_functions:
                self.test_obj.yakshaAssert("TestFormattingAndComposition", False, "functional")
                print("TestFormattingAndComposition = Failed")
                return
            
            # Track test results
            test_results = {}
            
            file_system = safely_call_function(self.module_obj, "create_sample_file_system")
            if file_system is None:
                test_results["file_system_available"] = False
                # Create fallback file system
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
                test_results["file_system_available"] = True
            
            # Test file size formatting
            format_zero = safely_call_function(self.module_obj, "format_file_size", 0)
            test_results["format_zero"] = (format_zero == "0 B")
            
            format_500 = safely_call_function(self.module_obj, "format_file_size", 500)
            test_results["format_bytes"] = (format_500 == "500 B")
            
            format_1024 = safely_call_function(self.module_obj, "format_file_size", 1024)
            test_results["format_kb"] = (format_1024 is not None and "1.00 KB" in format_1024)
            
            format_mb = safely_call_function(self.module_obj, "format_file_size", 1048576)
            test_results["format_mb"] = (format_mb is not None and "1.00 MB" in format_mb)
            
            format_gb = safely_call_function(self.module_obj, "format_file_size", 1073741824)
            test_results["format_gb"] = (format_gb is not None and "1.00 GB" in format_gb)
            
            # Test intermediate sizes
            format_2500 = safely_call_function(self.module_obj, "format_file_size", 2500)
            test_results["format_intermediate"] = (format_2500 is not None and "2.44 KB" in format_2500)
            
            format_1500000 = safely_call_function(self.module_obj, "format_file_size", 1500000)
            test_results["format_large"] = (format_1500000 is not None and "1.43 MB" in format_1500000)
            
            # Test function composition - calculate total PDF file sizes
            pdf_files = safely_call_function(self.module_obj, "find_by_extension", "", "pdf", file_system)
            if pdf_files is not None:
                total_pdf_size = 0
                
                for pdf_path in pdf_files:
                    # Navigate through the file system to get the file size
                    parts = pdf_path.split("/")
                    current = file_system
                    
                    try:
                        for part in parts[:-1]:  # Navigate to the directory
                            if part and part in current:
                                current = current[part]
                        
                        filename = parts[-1]
                        if filename in current and isinstance(current[filename], int):
                            total_pdf_size += current[filename]
                    except Exception:
                        pass
                
                # Expected: resume.pdf (520000) + report.pdf (750000) + book1.pdf (12000000) + book2.pdf (9500000) = 22770000
                test_results["pdf_composition"] = (total_pdf_size == 22770000)
            else:
                test_results["pdf_composition"] = False
            
            # Test composition of search and largest functions
            largest_10 = safely_call_function(self.module_obj, "find_largest_files", "", 10, file_system)
            if largest_10 is not None:
                docx_count = 0
                for item in largest_10:
                    if isinstance(item, tuple) and len(item) > 0 and isinstance(item[0], str):
                        if item[0].endswith(".docx"):
                            docx_count += 1
                
                test_results["largest_composition"] = (docx_count in [0, 1, 2])
            else:
                test_results["largest_composition"] = False
            
            # Check if most tests passed
            passed_tests = sum(1 for result in test_results.values() if result)
            total_tests = len(test_results)
            success_rate = passed_tests / total_tests
            
            if success_rate >= 0.8:  # 80% pass rate
                self.test_obj.yakshaAssert("TestFormattingAndComposition", True, "functional")
                print("TestFormattingAndComposition = Passed")
            else:
                self.test_obj.yakshaAssert("TestFormattingAndComposition", False, "functional")
                print("TestFormattingAndComposition = Failed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestFormattingAndComposition", False, "functional")
            print("TestFormattingAndComposition = Failed")

if __name__ == '__main__':
    unittest.main()