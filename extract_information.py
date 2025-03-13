import json
import os

from bs4 import BeautifulSoup


def extract_data(extract_type, target_name,base_url):
    """
    Extracts data from a JSON file containing HTML content.

    Args:
    - extract_type (str): The type of extraction ('class' or 'id').
    - target_name (str): The name of the class or id to extract.
    - input_json (str): The input JSON file containing HTML content (default 'webscrap.json').
    - output_json (str): The output JSON file where extracted information will be saved (default 'extracted_info.json').

    Returns:
    - None
    """
    folder_name = base_url.split("://")[1]  # Splits at '://' and takes the second part
    folder_path = f"Output/{folder_name}"
    input_json = f"{folder_path}/webscrap.json"
    output_json = f"{folder_path}/extracted_info.json"

    # Load the JSON file
    try:
        with open(input_json, "r", encoding="utf-8") as f:
            all_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {input_json} was not found.")
        return
    except json.JSONDecodeError:
        print("Error: Failed to decode the JSON file.")
        return

    # Validate extraction type
    if extract_type not in ["class", "id"]:
        print("Invalid extraction type. Please use 'class' or 'id'.")
        return

    # Store extracted information
    extracted_data = []
    seq_counter = 1

    # Parse HTML content and extract information
    for url, html_content in all_data.items():
        soup = BeautifulSoup(html_content, "html.parser")

        if extract_type == "class":
            # Find all elements with the specified class
            elements = soup.find_all(class_=target_name)
        elif extract_type == "id":
            # Find the element with the specified id
            element = soup.find(id=target_name)
            elements = [element] if element else []

        # Extract text from the elements
        for element in elements:
            extracted_data.append({
                "seq": seq_counter,  # Add sequence number
                "url": url,
                "text": element.get_text(strip=True)
            })
            seq_counter += 1  # Increment the sequence counter

    # Save the extracted information to a JSON file
    try:
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(extracted_data, f, ensure_ascii=False, indent=4)
        print(f"Extracted information saved to {output_json}")
    except IOError:
        print(f"Error: Could not write to {output_json}.")


def get_output_directory(file_path):
    """
    Extracts the directory path from a full file path and ensures it ends with a slash.

    Args:
        file_path (str): Full path to a file (e.g., 'C:/path/to/file.json')

    Returns:
        str: Directory path ending with slash (e.g., 'C:/path/to/')
    """
    # Get the directory path using os.path
    directory = os.path.dirname(file_path)

    # Convert backslashes to forward slashes for consistency
    directory = directory.replace('\\', '/')

    # Add trailing slash if not present
    if not directory.endswith('/'):
        directory += '/'

    return directory


def extract_data_from_file(extract_type, target_name,filepath):
    """
    Extracts data from a JSON file containing HTML content.

    Args:
    - extract_type (str): The type of extraction ('class' or 'id').
    - target_name (str): The name of the class or id to extract.
    - input_json (str): The input JSON file containing HTML content (default 'webscrap.json').
    - output_json (str): The output JSON file where extracted information will be saved (default 'extracted_info.json').

    Returns:
    - None
    """
    # folder_name = base_url.split("://")[1]  # Splits at '://' and takes the second part
    # folder_path = f"Output/{folder_name}"
    input_json = filepath
    folder_path = get_output_directory(input_json)
    output_json = f"{folder_path}/extracted_info1.json"

    # Load the JSON file
    try:
        with open(input_json, "r", encoding="utf-8") as f:
            all_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {input_json} was not found.")
        return
    except json.JSONDecodeError:
        print("Error: Failed to decode the JSON file.")
        return

    # Validate extraction type
    if extract_type not in ["class", "id"]:
        print("Invalid extraction type. Please use 'class' or 'id'.")
        return

    # Store extracted information
    extracted_data = []
    seq_counter = 1

    # Parse HTML content and extract information
    for url, html_content in all_data.items():
        soup = BeautifulSoup(html_content, "html.parser")

        if extract_type == "class":
            # Find all elements with the specified class
            elements = soup.find_all(class_=target_name)
        elif extract_type == "id":
            # Find the element with the specified id
            element = soup.find(id=target_name)
            elements = [element] if element else []

        # Extract text from the elements
        for element in elements:
            extracted_data.append({
                "seq": seq_counter,  # Add sequence number
                "url": url,
                "text": element.get_text(strip=True)
            })
            seq_counter += 1  # Increment the sequence counter

    # Save the extracted information to a JSON file
    try:
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(extracted_data, f, ensure_ascii=False, indent=4)
        print(f"Extracted information saved to {output_json}")
    except IOError:
        print(f"Error: Could not write to {output_json}.")

