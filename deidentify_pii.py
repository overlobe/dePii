#!/usr/bin/env python3
"""
PII Deidentification Script for Markdown Files

This script searches through markdown files in a directory and replaces
personally identifiable information (PII) such as email addresses, names,
phone numbers, and other sensitive data with anonymized placeholders.
"""

import re
import os
import argparse
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PIIDeidentifier:
    def __init__(self):
        # Email pattern - matches most common email formats
        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )
        
        # Phone number patterns - Australian and international formats
        self.phone_patterns = [
            re.compile(r'\+61\s?\d+\s?\d+\s?\d+'),  # +61 formats
            re.compile(r'\b0\d{3}\s?\d{3}\s?\d{3}\b'),  # Australian mobile 0xxx xxx xxx
            re.compile(r'\b\d{9,10}\b'),  # Simple 9-10 digit numbers
            re.compile(r'\b\(\d{2}\)\s?\d{4}\s?\d{4}\b'),  # (02) 1234 5678
            re.compile(r'\b0[2-9]\s?\d{4}\s?\d{4}\b'),  # Landline 0x xxxx xxxx
        ]
        
        # Specific names found in the data - more targeted approach
        self.specific_names = {
            'Zoe W': 'Participant A',
            'James B': 'Participant B', 
            'Jason W': 'Participant C',
            'John Smith': 'Participant D'
        }
        
        # Common first names to replace
        self.common_names = [
            'Zoe', 'James', 'Jason', 'John', 'Jane', 'Michael', 'Sarah', 
            'David', 'Lisa', 'Robert', 'Mary', 'William', 'Patricia'
        ]
        
        # ID numbers and sensitive identifiers
        self.id_patterns = [
            re.compile(r'\bID:\s*\d+\b'),
            re.compile(r'\bMobile:\s*\d+\b'),
        ]
        
        # Counter for generating unique replacements
        self.email_counter = 1
        self.name_counter = 1
        self.phone_counter = 1
        self.id_counter = 1
        
        # Store mappings to ensure consistency
        self.email_mappings = {}
        self.name_mappings = {}
        self.phone_mappings = {}
        self.id_mappings = {}

    def deidentify_emails(self, text, file_identifier="participant"):
        """Replace email addresses with anonymized versions using file identifier"""
        def replace_email(match):
            email = match.group(0)
            if email not in self.email_mappings:
                domain = email.split('@')[1]
                if 'gmail.com' in domain:
                    replacement = f"{file_identifier}@gmail.com"
                elif 'hotmail.com' in domain:
                    replacement = f"{file_identifier}@hotmail.com"
                else:
                    replacement = f"{file_identifier}@example.com"
                self.email_mappings[email] = replacement
            return self.email_mappings[email]
        
        return self.email_pattern.sub(replace_email, text)

    def deidentify_phones(self, text):
        """Replace phone numbers with anonymized versions"""
        def replace_phone(match):
            phone = match.group(0)
            if phone not in self.phone_mappings:
                # Generate a fake phone number maintaining format
                if phone.startswith('0'):
                    replacement = f"0XXX XXX {str(self.phone_counter).zfill(3)}"
                elif '+61' in phone:
                    replacement = f"+61 XXX XXX {str(self.phone_counter).zfill(3)}"
                else:
                    replacement = f"XXX XXX {str(self.phone_counter).zfill(3)}"
                self.phone_mappings[phone] = replacement
                self.phone_counter += 1
            return self.phone_mappings[phone]
        
        for pattern in self.phone_patterns:
            text = pattern.sub(replace_phone, text)
        return text

    def deidentify_names(self, text, file_identifier="Participant"):
        """Replace specific names with anonymized versions using file identifier"""
        # Replace specific known full names first
        for original_name in self.specific_names.keys():
            text = re.sub(re.escape(original_name), file_identifier, text, flags=re.IGNORECASE)
        
        # Handle standalone first names
        common_first_names = ['Zoe', 'James', 'Jason', 'John', 'Jane', 'Michael', 'Sarah', 
                             'David', 'Lisa', 'Robert', 'Mary', 'William', 'Patricia']
        
        for name in common_first_names:
            # Replace standalone first names (not followed by known surnames)
            text = re.sub(rf'\b{name}\b(?!\s+[A-Z])', file_identifier, text)
        
        return text

    def deidentify_ids(self, text):
        """Replace ID numbers and identifiers"""
        def replace_id(match):
            id_text = match.group(0)
            if id_text not in self.id_mappings:
                if 'ID:' in id_text:
                    replacement = f"ID: {str(self.id_counter).zfill(6)}"
                elif 'Mobile:' in id_text:
                    replacement = f"Mobile: XXXX{str(self.id_counter).zfill(3)}"
                else:
                    replacement = f"ID_{self.id_counter}"
                self.id_mappings[id_text] = replacement
                self.id_counter += 1
            return self.id_mappings[id_text]
        
        for pattern in self.id_patterns:
            text = pattern.sub(replace_id, text)
        return text

    def deidentify_text(self, text, file_identifier="participant"):
        """Apply all deidentification patterns to text"""
        text = self.deidentify_emails(text, file_identifier.lower())
        text = self.deidentify_phones(text)
        text = self.deidentify_names(text, file_identifier.upper())
        text = self.deidentify_ids(text)
        return text

    def process_file(self, file_path, output_dir=None, in_place=False):
        """Process a single markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract filename without extension to use as identifier
            file_stem = Path(file_path).stem
            # Remove "deidentified_" prefix if it exists
            if file_stem.startswith('deidentified_'):
                file_stem = file_stem[13:]
            
            deidentified_content = self.deidentify_text(content, file_stem)
            
            if in_place:
                output_path = file_path
            elif output_dir:
                output_path = Path(output_dir) / f"deidentified_{Path(file_path).name}"
            else:
                output_path = Path(file_path).parent / f"deidentified_{Path(file_path).name}"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(deidentified_content)
            
            logger.info(f"Processed: {file_path} -> {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return None

    def process_directory(self, directory, output_dir=None, in_place=False):
        """Process all markdown files in a directory"""
        directory = Path(directory)
        if not directory.exists():
            raise ValueError(f"Directory {directory} does not exist")
        
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(exist_ok=True)
        
        markdown_files = list(directory.glob('*.md'))
        if not markdown_files:
            logger.warning(f"No markdown files found in {directory}")
            return []
        
        processed_files = []
        for md_file in markdown_files:
            result = self.process_file(md_file, output_dir, in_place)
            if result:
                processed_files.append(result)
        
        logger.info(f"Processed {len(processed_files)} files")
        return processed_files

def main():
    parser = argparse.ArgumentParser(description='Deidentify PII in markdown files')
    parser.add_argument('input_path', help='Input file or directory path')
    parser.add_argument('--output-dir', '-o', help='Output directory (default: same as input)')
    parser.add_argument('--in-place', '-i', action='store_true', 
                       help='Modify files in place (overwrites original files)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    deidentifier = PIIDeidentifier()
    input_path = Path(args.input_path)
    
    try:
        if input_path.is_file():
            if input_path.suffix.lower() == '.md':
                deidentifier.process_file(input_path, args.output_dir, args.in_place)
            else:
                logger.error("Input file must be a markdown (.md) file")
        elif input_path.is_dir():
            deidentifier.process_directory(input_path, args.output_dir, args.in_place)
        else:
            logger.error(f"Input path {input_path} does not exist")
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())