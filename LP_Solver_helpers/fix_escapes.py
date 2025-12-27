"""
Utility script to fix incorrectly escaped quotes in Python files.
Removes backslash-quote (\\") and backslash-backslash-n (\\\\n) patterns.
"""

import os

def fix_escape_characters(filename):
    """Fix escape characters in a Python file."""
    print(f"Processing: {filename}")
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count issues before fix
    backslash_quotes = content.count('\\"')
    backslash_ns = content.count('\\\\n')
    
    print(f"  Found {backslash_quotes} backslash-quotes")
    print(f"  Found {backslash_ns} backslash-backslash-n sequences")
    
    # Fix the escapes
    #Replace \\" with just "
    content = content.replace('\\"', '"')
    
    # Replace \\\\n with \\n (for newlines in strings)
    content = content.replace('\\\\n', '\\n')
    
    # Backup original
    backup_name = filename + '.backup'
    with open(backup_name, 'w', encoding='utf-8') as f:
        f.write(open(filename, 'r', encoding='utf-8').read())
    print(f"  Backup saved as: {backup_name}")
    
    # Write fixed content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ Fixed and saved: {filename}\n")
    
    return True

if __name__ == "__main__":
    files_to_fix = [
        'sensitivity_module.py',
        'integrated_solver.py'
    ]
    
    for filename in files_to_fix:
        if os.path.exists(filename):
            try:
                fix_escape_characters(filename)
            except Exception as e:
                print(f"  ✗ Error fixing {filename}: {e}\n")
        else:
            print(f"  ✗ File not found: {filename}\n")
    
    print("=" * 60)
    print("Escape character fixes complete!")
    print("=" * 60)
