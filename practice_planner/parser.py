def parse_file(filename):
    sections = {}
    current_section = None
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("#"):
                    current_section = line[1:].strip()
                    sections[current_section] = []
                elif line.startswith("-") and current_section:
                    sections[current_section].append(line[1:].strip())
    except FileNotFoundError:
        sections = {}
    return sections
