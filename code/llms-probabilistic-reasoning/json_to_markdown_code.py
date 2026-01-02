#!/usr/bin/env python3
"""
Convert JSON result files to markdown format for code results.
Extracts reasoning and content fields and creates markdown files.
Transforms <code></code> tags into Python code blocks.
"""

import json
import re
from pathlib import Path


def convert_code_tags_to_markdown(content):
    """Convert <code></code> tags to markdown Python code blocks."""
    # Pattern to match <code>...</code> tags (including multiline)
    pattern = r'<code>(.*?)</code>'
    
    def replace_code(match):
        code_content = match.group(1).strip()
        # Remove leading/trailing newlines from code content
        code_content = code_content.strip('\n')
        return f'```python\n{code_content}\n```'
    
    # Replace all <code></code> tags with markdown code blocks
    converted = re.sub(pattern, replace_code, content, flags=re.DOTALL)
    
    return converted


def process_json_to_markdown(json_path, output_dir):
    """Convert a single JSON file to markdown format."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract fields
    model = data.get('model', 'unknown')
    reasoning = data.get('reasoning', '')
    content = data.get('content', '')
    
    # Convert <code></code> tags to markdown code blocks
    content = convert_code_tags_to_markdown(content)
    
    # Create title from model name
    title = f"# {model}\n"
    
    # Build markdown content
    markdown_content = title + "\n"
    markdown_content += "## Reasoning\n\n"
    markdown_content += reasoning + "\n\n"
    markdown_content += "----\n\n"
    markdown_content += "## Content\n\n"
    markdown_content += content + "\n"
    
    # Create output filename (same as input but with .md extension)
    json_filename = Path(json_path).stem
    output_path = output_dir / f"{json_filename}.md"
    
    # Write markdown file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Created: {output_path}")


def main():
    """Process all JSON files in subdirectories of the results directory."""
    # Define paths
    script_dir = Path(__file__).parent
    results_dir = script_dir / 'results'
    output_base_dir = script_dir / 'results_md'
    
    # Create output base directory if it doesn't exist
    output_base_dir.mkdir(exist_ok=True)
    
    # Find all JSON files in subdirectories
    json_files = list(results_dir.glob('**/*.json'))
    
    if not json_files:
        print(f"No JSON files found in {results_dir}")
        return
    
    print(f"Found {len(json_files)} JSON file(s)")
    
    # Process each JSON file
    for json_file in json_files:
        try:
            # Get relative path from results_dir to maintain subdirectory structure
            relative_path = json_file.relative_to(results_dir)
            subdirectory = relative_path.parent
            
            # Create corresponding output subdirectory
            output_subdir = output_base_dir / subdirectory
            output_subdir.mkdir(parents=True, exist_ok=True)
            
            process_json_to_markdown(json_file, output_subdir)
        except Exception as e:
            print(f"Error processing {json_file}: {e}")
    
    print(f"\nDone! Markdown files created in {output_base_dir}")


if __name__ == '__main__':
    main()


