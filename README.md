# PII Deidentification Tool for Markdown Files

A Python script for automatically detecting and replacing personally identifiable information (PII) in markdown files with anonymized placeholders.

**Repository**: [https://github.com/overlobe/dePii](https://github.com/overlobe/dePii)

## Features

- **Filename-Based Replacement**: Uses the source filename to create consistent, traceable placeholders
- **Email Address Detection**: Replaces email addresses with filename-based versions (e.g., `p01@gmail.com`)
- **Name Replacement**: Identifies and replaces participant names with filename identifiers (e.g., `P01`)
- **Phone Number Anonymization**: Handles various phone number formats (Australian and international)
- **ID Number Masking**: Replaces ID numbers and mobile numbers with anonymized versions
- **Batch Processing**: Process single files or entire directories
- **Consistent Mapping**: Maintains consistent replacements within each file
- **Flexible Output**: Save to new files or modify originals in-place

## Installation

### Quick Start
```bash
# Clone the repository
git clone https://github.com/overlobe/dePii.git
cd dePii

# Make executable
chmod +x deidentify_pii.py
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Usage

### Command Line Interface

```bash
python3 deidentify_pii.py [input_path] [options]
```

#### Arguments
- `input_path`: Path to a markdown file or directory containing markdown files

#### Options
- `--output-dir, -o DIR`: Specify output directory (default: same as input)
- `--in-place, -i`: Modify files in place (overwrites original files)
- `--verbose, -v`: Enable verbose logging
- `--help, -h`: Show help message

### Examples

#### Process a single file
```bash
# Create deidentified copy
python3 deidentify_pii.py document.md

# Save to specific directory
python3 deidentify_pii.py document.md --output-dir ./clean

# Modify file in place
python3 deidentify_pii.py document.md --in-place
```

#### Process all markdown files in a directory
```bash
# Process all .md files, save to 'deidentified' folder
python3 deidentify_pii.py ./research_files --output-dir ./deidentified

# Process with verbose output
python3 deidentify_pii.py ./research_files --verbose

# Modify all files in place
python3 deidentify_pii.py ./research_files --in-place
```

## PII Detection Patterns

The tool uses the filename (without extension) to create consistent, traceable placeholders:

### Email Addresses
- **Input**: `john.doe@gmail.com`, `researcher@university.edu` (in file `P01.md`)
- **Output**: `p01@gmail.com`, `p01@example.com`

### Names
- **Input**: `Zoe W`, `James B`, `Jason W` (in file `P01.md`)
- **Output**: `P01`, `P01`, `P01`

### Phone Numbers
- **Input**: `0481 119 861`, `+61 2 1234 5678`, `448942703`
- **Output**: `XXX XXX 001`, `+61 XXX XXX 002`, `XXX XXX 003`

### ID Numbers
- **Input**: `ID: 592389`, `Mobile: 448942703`
- **Output**: `ID: 000001`, `Mobile: XXXX001`

## Safety Features

- **Backup Recommended**: Always backup original files before processing
- **Filename-Based Traceability**: Replacements are tied to source files for easy tracking
- **Consistent Mapping**: Same PII instances get same replacements within each file
- **Preservation**: Maintains markdown formatting and structure
- **Logging**: Detailed logging of all processing activities

## Limitations

- **Context Awareness**: Limited understanding of context; may occasionally replace non-PII text
- **Pattern Based**: Relies on regex patterns; may miss unusual formats
- **False Positives**: May replace legitimate text that matches PII patterns
- **Language**: Optimized for English text

## File Structure

```
dePii/
├── deidentify_pii.py          # Main script
├── README.md                  # This documentation
├── requirements.txt           # Python dependencies
├── setup.py                   # Package installation
├── examples/                  # Example files
│   ├── sample_input.md
│   └── sample_output.md
└── tests/                     # Test cases
    └── test_deidentify.py
```

## Development

### Running Tests
```bash
python3 -m pytest tests/
```

### Adding New PII Patterns

To add new PII detection patterns, modify the `PIIDeidentifier` class:

```python
# Add new pattern in __init__
self.new_pattern = re.compile(r'your_regex_pattern')

# Add corresponding deidentification method
def deidentify_new_type(self, text):
    # Implementation here
    return text

# Update main deidentify_text method
def deidentify_text(self, text):
    text = self.deidentify_emails(text)
    text = self.deidentify_phones(text)
    text = self.deidentify_names(text)
    text = self.deidentify_ids(text)
    text = self.deidentify_new_type(text)  # Add this line
    return text
```

## Security Considerations

- **Sensitive Data**: Always review output files to ensure complete deidentification
- **Backup**: Keep secure backups of original files
- **Access Control**: Limit access to both original and processed files
- **Validation**: Manually verify critical deidentification results

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-pattern`)
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or contributions:
- Open an issue on [GitHub](https://github.com/overlobe/dePii/issues)
- Submit a pull request

## Changelog

### v1.0.0
- Initial release
- Basic PII detection for emails, names, phones, IDs
- Command line interface
- Batch processing support