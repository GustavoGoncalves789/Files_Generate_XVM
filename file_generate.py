import re

def sanitize_filename(name):
    # Replace special characters with underscores
    return re.sub(r'[^\w]', '_', name)

def generate_section_files(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        section_title = None
        section_content = []

        for line in lines:
            if line.strip():  # Non-empty line
                if line.startswith('\t'):  # Content line
                    section_content.append(line)
                else:  # Section title line
                    if section_title:
                        # Write content to file
                        with open(f"{sanitize_filename(section_title.strip())}.xmv", 'w') as section_file:
                            section_file.write(f"{section_title.strip()}\n")
                            section_file.writelines(section_content)
                    section_title = line.strip()
                    section_content = []

        # Write content for the last section
        if section_title and section_content:
            with open(f"{sanitize_filename(section_title.strip())}.xmv", 'w') as section_file:
                section_file.write(f"title = {section_title.strip()}\n")
                section_file.writelines(section_content)

# Usage example
generate_section_files("model_teste.xmv")
