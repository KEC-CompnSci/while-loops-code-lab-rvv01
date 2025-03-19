import io
import sys
import os
import unittest
from unittest.mock import patch
import importlib.util

class TestWhileLoops(unittest.TestCase):
    
    def setUp(self):
        # Add the src directory to the system path
        src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        # Load the assignment module
        self.original_stdout = sys.stdout
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output
    
    def tearDown(self):
        # Reset stdout
        sys.stdout = self.original_stdout
    
    def reload_assignment(self):
        # Dynamically load or reload the assignment module
        try:
            if 'assignment' in sys.modules:
                importlib.reload(sys.modules['assignment'])
            else:
                spec = importlib.util.spec_from_file_location("assignment", 
                    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'assignment.py'))
                assignment = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(assignment)
                sys.modules['assignment'] = assignment
            return True
        except Exception as e:
            self.fail(f"Error importing assignment.py: {str(e)}")
            return False
    
    def test_count_by_twos(self):
        # Clear captured output
        self.captured_output.seek(0)
        self.captured_output.truncate(0)
        
        # Reload and run the assignment
        self.reload_assignment()
        
        # Get the output
        output = self.captured_output.getvalue()
        
        # Check if all even numbers from 2 to 50 are in the output
        expected_numbers = [str(i) for i in range(2, 51, 2)]
        for num in expected_numbers:
            self.assertIn(num, output, f"Missing number {num} in the output")
        
        # Check that we have the right number of even numbers (25 numbers from 2 to 50, counting by 2)
        # We split by lines and filter out empty lines and the "Task complete" message
        number_lines = [line.strip() for line in output.split('\n') 
                        if line.strip() and 'Task' not in line]
        numbers_found = 0
        for line in number_lines:
            for num in expected_numbers:
                if num in line:
                    numbers_found += 1
                    break
        
        self.assertEqual(len(expected_numbers), numbers_found, 
                        f"Expected {len(expected_numbers)} numbers, but found {numbers_found}")
    
    def test_grid_pattern(self):
        # Clear captured output
        self.captured_output.seek(0)
        self.captured_output.truncate(0)
        
        # Reload and run the assignment
        self.reload_assignment()
        
        # Get the output
        output = self.captured_output.getvalue()
        
        # Remove the "Task complete" lines and split by newlines
        lines = [line for line in output.split('\n') if 'Task' not in line and line.strip()]
        
        # Check that we have exactly 5 rows in the grid
        grid_lines = [line for line in lines if '#' in line]
        self.assertEqual(5, len(grid_lines), f"Expected 5 rows in the grid, found {len(grid_lines)}")
        
        # Check that each row has exactly 5 # symbols
        for i, line in enumerate(grid_lines):
            hash_count = line.count('#')
            self.assertEqual(5, hash_count, f"Row {i+1} should have 5 # symbols, found {hash_count}")

if __name__ == '__main__':
    unittest.main()