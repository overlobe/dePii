#!/usr/bin/env python3
"""
Test suite for PII Deidentification Tool
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add parent directory to path to import the main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deidentify_pii import PIIDeidentifier


class TestPIIDeidentifier(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.deidentifier = PIIDeidentifier()
    
    def test_email_deidentification(self):
        """Test email address replacement"""
        text = "Contact me at john.doe@gmail.com or researcher@university.edu"
        result = self.deidentifier.deidentify_emails(text, "testfile")
        
        self.assertNotIn("john.doe@gmail.com", result)
        self.assertNotIn("researcher@university.edu", result)
        self.assertIn("testfile@", result.lower())
    
    def test_phone_deidentification(self):
        """Test phone number replacement"""
        text = "Call me at +61 2 1234 5678 or 0412 345 678"
        result = self.deidentifier.deidentify_phones(text)
        
        self.assertNotIn("+61 2 1234 5678", result)
        self.assertNotIn("0412 345 678", result)
        self.assertIn("XXX", result)
    
    def test_name_deidentification(self):
        """Test name replacement"""
        text = "John Smith and Zoe W attended the meeting"
        result = self.deidentifier.deidentify_names(text, "TESTFILE")
        
        self.assertNotIn("John Smith", result)
        self.assertNotIn("Zoe W", result)
        self.assertIn("TESTFILE", result)
    
    def test_id_deidentification(self):
        """Test ID number replacement"""
        text = "ID: 123456 and Mobile: 0412345678"
        result = self.deidentifier.deidentify_ids(text)
        
        self.assertNotIn("123456", result)
        self.assertIn("000001", result)
    
    def test_consistent_mapping(self):
        """Test that same PII gets same replacement"""
        text1 = "Email john@example.com"
        text2 = "Contact john@example.com again"
        
        result1 = self.deidentifier.deidentify_emails(text1, "testfile")
        result2 = self.deidentifier.deidentify_emails(text2, "testfile")
        
        # Extract the replacement email from both results
        import re
        email_pattern = re.compile(r'testfile@\w+\.com')
        match1 = email_pattern.search(result1)
        match2 = email_pattern.search(result2)
        
        self.assertIsNotNone(match1)
        self.assertIsNotNone(match2)
        self.assertEqual(match1.group(), match2.group())
    
    def test_full_deidentification(self):
        """Test complete deidentification process"""
        text = """
        # Research Data
        Name: John Smith
        Email: john.smith@gmail.com
        Phone: +61 2 1234 5678
        ID: 987654
        
        John shared his email john.smith@gmail.com for follow-up.
        """
        
        result = self.deidentifier.deidentify_text(text, "testfile")
        
        # Check that PII is removed
        self.assertNotIn("John Smith", result)
        self.assertNotIn("john.smith@gmail.com", result)
        self.assertNotIn("+61 2 1234 5678", result)
        self.assertNotIn("987654", result)
        
        # Check that replacements are present
        self.assertIn("TESTFILE", result)
        self.assertIn("testfile@", result.lower())
    
    def test_file_processing(self):
        """Test processing of actual files"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("""
            # Test Document
            Participant: Jane Doe
            Email: jane@example.com
            Phone: 0412 123 456
            """)
            temp_file = f.name
        
        try:
            # Process the file
            output_file = self.deidentifier.process_file(temp_file)
            self.assertIsNotNone(output_file)
            
            # Check output exists
            self.assertTrue(os.path.exists(output_file))
            
            # Check content is deidentified
            with open(output_file, 'r') as f:
                content = f.read()
                self.assertNotIn("jane@example.com", content)
                self.assertNotIn("0412 123 456", content)
            
            # Clean up output file
            os.unlink(output_file)
            
        finally:
            # Clean up temp file
            os.unlink(temp_file)
    
    def test_markdown_preservation(self):
        """Test that markdown formatting is preserved"""
        text = """
        # Main Header
        
        ## Sub Header
        
        - List item with john@example.com
        - Another item
        
        **Bold text** with phone +61 2 1234 5678
        
        > Quote block
        
        ```code block```
        """
        
        result = self.deidentifier.deidentify_text(text, "testfile")
        
        # Check markdown elements are preserved
        self.assertIn("# Main Header", result)
        self.assertIn("## Sub Header", result)
        self.assertIn("- List item", result)
        self.assertIn("**Bold text**", result)
        self.assertIn("> Quote block", result)
        self.assertIn("```code block```", result)


class TestCLIInterface(unittest.TestCase):
    """Test command line interface functionality"""
    
    def test_help_output(self):
        """Test that help can be displayed"""
        import subprocess
        import sys
        
        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'deidentify_pii.py')
        result = subprocess.run([sys.executable, script_path, '--help'], 
                              capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("Deidentify PII in markdown files", result.stdout)


if __name__ == '__main__':
    unittest.main()