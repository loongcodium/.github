import csv
import re
import requests
import urllib.parse
from typing import Dict, List, Tuple
from tqdm import tqdm


# Store extension info, avoid repeated requests
_EXTENSION_CACHE = {}


def update_readme_table(readme_path: str, csv_path: str) -> None:
    """
    Update the extensions table in README using comment markers.
    
    Args:
        readme_path: Path to README file
        csv_path: Path to CSV data file
    
    Raises:
        ValueError: If table start or end markers are not found in README
    """
    # Read README file
    with open(readme_path, 'r', encoding='utf-8') as file:
        readme_content = file.read()
    
    # Find the table start and end markers
    start_marker = "<!-- table_start -->"
    end_marker = "<!-- table_end -->"
    
    start_pos = readme_content.find(start_marker)
    end_pos = readme_content.find(end_marker)
    if start_pos == -1:
        raise ValueError(f"Table start marker '{start_marker}' not found in README")
    
    if end_pos == -1:
        raise ValueError(f"Table end marker '{end_marker}' not found in README")
    
    if end_pos <= start_pos:
        raise ValueError("Table end marker appears before start marker in README")
    
    # Include the markers in the replacement
    start_pos_with_marker = start_pos
    end_pos_with_marker = end_pos + len(end_marker)
    
    # Read extension data
    extensions = read_extensions_csv(csv_path)

    # Generate table content
    rows_with_names = []
    for ext in tqdm(extensions, desc="Processing extensions", unit="ext"):
        display_name, row = generate_table_row(
            ext['original_id'],
            ext['status'],
            ext['actual_ids'],
            ext['notes']
        )
        rows_with_names.append((display_name, row))
    
    # Sort by display name (case-insensitive)
    rows_with_names.sort(key=lambda x: x[0].lower())
    
    # Extract sorted rows
    table_lines = [row for _, row in rows_with_names]

    # Create the full table with headers
    table_content = "| Extension Name | Status | Notes | Latest Version |\n"
    table_content += "|----------------|--------|-------|----------------|\n"
    table_content += "\n".join(table_lines)
    
    # Replace the table section (including markers)
    updated_content = (
        readme_content[:start_pos_with_marker] +
        start_marker + "\n" + table_content + "\n" + end_marker +
        readme_content[end_pos_with_marker:]
    )
    
    # Write updated README
    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)


def read_extensions_csv(file_path: str) -> List[Dict[str, str]]:
    """
    Read extensions data from CSV file.
    
    Args:
        file_path: Path to CSV file
    
    Returns:
        List of extension data dictionaries
    
    Raises:
        ValueError: If CSV file has invalid format
    """
    extensions = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            
            reader = csv.DictReader(file, skipinitialspace=True)
            
            required_columns = ['original_id', 'status', 'actual_ids', 'notes']
            if not reader.fieldnames:
                raise ValueError("CSV file is empty or has no headers")
            
            missing_columns = [col for col in required_columns if col not in reader.fieldnames]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            for row_num, row in enumerate(reader, start=2): 
                try:
                    cleaned_row = {}
                    for key in required_columns:
                        value = row.get(key, '')
                        if isinstance(value, str):
                            cleaned_row[key] = value.strip()
                        else:
                            cleaned_row[key] = value
                    
                    status = cleaned_row['status']
                    if status not in ['0', '1', '2', '3']:
                        raise ValueError(f"Invalid status code '{status}' at row {row_num}")
                    
                    extensions.append(cleaned_row)
                    
                except Exception as e:
                    raise ValueError(f"Error processing row {row_num}: {e}")
    
    except FileNotFoundError:
        raise ValueError(f"CSV file not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")
    
    return extensions


def generate_table_row(original_id: str, status: str, actual_ids: str, notes: str) -> Tuple[str, str]:
    """
    Generate Markdown table row for an extension.
    
    Args:
        original_id: Original extension ID
        status: Status code
        actual_ids: List of actual available extension IDs
        notes: Notes/instructions
    
    Returns:
        Tuple of (display_name, markdown_formatted_table_row)
    """
    # Get original extension info
    try:
        original_info = get_extension_info(original_id)
        original_name = original_info["name"]
        original_uri = original_info["uri"]
    except ValueError:
        original_name = original_id
        original_uri = f"https://marketplace.visualstudio.com/items?itemName={original_id}"
    
    extension_link = f"[{original_name}]({original_uri})"
    status_display = generate_status_display(status)
    version_badge = generate_version_badge(original_id, actual_ids, status)
    notes_display = generate_notes_display(actual_ids, status, notes)

    row_content = f"| {extension_link} | {status_display} | {notes_display} | {version_badge} |"
    return (original_name, row_content) # original_name is for table sorting.


def get_extension_info(extension_id: str) -> Dict[str, str]:
    """
    Get extension name and URI by extension ID.
    
    Args:
        extension_id: Extension ID in format like "ms-python.python"
    
    Returns:
        Dictionary with name and URI: {"name": "Python", "uri": "https://open-vsx.org/extension/ms-python/python"}
    
    Raises:
        ValueError: If extension cannot be found in either Open VSX or VSCode Marketplace
    """
    extension_id = extension_id.strip()
    
    # Check cache
    if extension_id in _EXTENSION_CACHE:
        return _EXTENSION_CACHE[extension_id]
    
    # Try Open VSX first
    if '.' in extension_id:
        namespace, ext_name = extension_id.split('.', 1)
        api_path = f"{namespace}/{ext_name}"
    else:
        api_path = extension_id

    url = f"https://open-vsx.org/api/{api_path}"
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()
        name = data.get("displayName", "")
        namespace = data.get("namespace", "")
        extension = data.get("name", "")
        
        if name and namespace and extension:
            uri = f"https://open-vsx.org/extension/{namespace}/{extension}"
            result = {"name": name, "uri": uri}
            _EXTENSION_CACHE[extension_id] = result
            return result

    # Fall back to VSCode Marketplace
    marketplace_url = f"https://marketplace.visualstudio.com/items?itemName={extension_id}"
    response = requests.get(marketplace_url, timeout=10)

    if response.status_code == 200:
        html = response.text
        match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        
        if match:
            title = match.group(1)
            if " - Visual Studio Marketplace" in title:
                name = title.replace(" - Visual Studio Marketplace", "").strip()
                result = {"name": name, "uri": marketplace_url}
                _EXTENSION_CACHE[extension_id] = result
                return result

    raise ValueError(f"Cannot find extension: {extension_id}")


def get_badge_url(extension_id: str, status_code: str, extension_name: str = "") -> str:
    """
    Generate version badge URL for an extension.
    
    Args:
        extension_id: Extension ID in format like "ms-python.python"
        status_code: Status code 0-3
        extension_name: Extension's name to be displayed as badge label
    
    Returns:
        shields.io badge URL
    """
    # Convert from dot-separated to slash-separated for Open VSX API
    if '.' in extension_id:
        namespace, ext_name = extension_id.split('.', 1)
        api_path = f"{namespace}/{ext_name}"
    else:
        api_path = extension_id

    status_cmap = {
        '0': 'brightgreen',
        '1': 'teal', 
        '2': 'blue',
        '3': 'red'
    }
    badge_color = status_cmap.get(status_code, 'grey')
    
    # URL encode the extension name for label
    encoded_label = urllib.parse.quote(extension_name) if extension_name else ""
        
    return f"https://img.shields.io/badge/dynamic/json?url=https://open-vsx.org/api/{api_path}&query=$.version&label={encoded_label}&color={badge_color}"


def generate_status_display(status_code: str) -> str:
    """
    Get status display with emoji and text.
    
    Args:
        status_code: Status code 0-3
    
    Returns:
        Status display string with emoji and text
    """
    status_map = {
        '0': '✅ Working',
        '1': '🚀 Ported', 
        '2': '🔄 Alternative',
        '3': '😭 Not Working'
    }
    return status_map.get(status_code, '❓ Unknown')


def generate_version_badge(original_id: str, actual_ids: str, status_code: str) -> str:
    """
    Generate version badge(s) for an extension.
    
    Args:
        original_id: Original extension ID
        actual_ids: Pipe-separated list of actual available extension IDs
        status_code: Status code 0-3
    
    Returns:
        Markdown formatted version badge(s)
    """
    # When no actual available extension
    if not actual_ids:
        # Generate badge for original extension
        badge = get_badge_url(original_id, status_code)
        return f'![version]({badge})'
    
    # Process single actual available extension
    elif "|" not in actual_ids:
        badge = get_badge_url(actual_ids, status_code)
        return f'![version]({badge})'
    
    # Process multiple actual available extensions
    else:
        actual_ids_list = [id.strip() for id in actual_ids.split('|')]
        badges = []
        for ext_id in actual_ids_list:
            ext_info = get_extension_info(ext_id)
            ext_name = ext_info["name"]
            badge = get_badge_url(ext_id, status_code, ext_name)
            badges.append(f'![version]({badge})')
        return ' '.join(badges)


def _generate_links_for_notes(actual_ids_list: List[str]) -> str:
    """
    Generate formatted links for notes section when multiple extensions are available.
    
    Args:
        actual_ids_list: List of actual extension IDs
    
    Returns:
        Formatted string with links
    """
    if not actual_ids_list:
        return ""
    
    links = []
    for ext_id in actual_ids_list:
        ext_info = get_extension_info(ext_id)
        name = ext_info["name"]
        uri = ext_info["uri"]
        links.append(f"[{name}]({uri})")
    
    if len(links) == 1:
        return links[0]
    elif len(links) == 2:
        return f"{links[0]} or {links[1]}"
    else:
        # Format as "A, B, or C"
        all_but_last = ", ".join(links[:-1])
        return f"{all_but_last}, or {links[-1]}"


def generate_notes_display(actual_ids: str, status_code: str, notes: str) -> str:
    """
    Generate formatted notes display for an extension.
    
    Args:
        actual_ids: Pipe-separated list of actual available extension IDs
        status_code: Status code 0-3
        notes: Original notes from CSV
    
    Returns:
        Formatted notes string
    """
    # When no actual available extension
    if not actual_ids:
        if status_code == "0":
            prefix = "Works out of the box."
        elif status_code == "3":
            prefix = "Unsupported architecture."
        else:
            raise ValueError("Please provide actual_ids if the extension is ported or has alternative!")
    # Process actual available extensions   
    else:
        actual_ids_list = [id.strip() for id in actual_ids.split('|')]
        # Generate prefix based on status code
        if status_code == "1":  # Ported
            prefix = f"Use {_generate_links_for_notes(actual_ids_list)} instead."
        elif status_code == "2":  # Alternative
            prefix = f"Use {_generate_links_for_notes(actual_ids_list)} instead."
        else:
            raise ValueError("Please do not provide actual_ids if the extension is working or not working!")
    # Combine prefix and notes
    if prefix and notes:
        return f"{prefix} {notes}"
    elif prefix:
        return prefix
    else:
        return notes


if __name__ == "__main__":
    update_readme_table(readme_path="profile/README.md", csv_path="scripts/extensions.csv")
