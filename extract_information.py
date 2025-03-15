import json
import os
from bs4 import BeautifulSoup


def parse_targets(raw_targets):
    """Parse user input into structured targets."""
    targets = []
    for part in raw_targets.split(','):
        part = part.strip()
        if '=' not in part:
            raise ValueError(f"Invalid target format: {part}")
        type_part, name_part = part.split('=', 1)
        type_code = type_part.strip().lower()
        if type_code not in ('c', 'i'):
            raise ValueError(f"Invalid type prefix: {type_part}")
        # Clean and validate name
        name = name_part.strip().strip('"\'').strip()
        if not name:
            raise ValueError(f"Empty target name in: {part}")
        targets.append({
            'type': 'class' if type_code == 'c' else 'id',
            'name': name
        })
    return targets


def extract_data(base_url, raw_targets):
    """Extract mixed classes/IDs from scraped data."""
    folder_name = base_url.split("://")[1]
    folder_path = f"Output/{folder_name}"
    input_json = f"{folder_path}/webscrap.json"
    output_json = f"{folder_path}/extracted_info.json"

    # Load data
    try:
        with open(input_json, "r", encoding="utf-8") as f:
            all_data = json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load data: {str(e)}")

    # Parse targets
    try:
        targets = parse_targets(raw_targets)
    except ValueError as e:
        raise RuntimeError(f"Invalid target input: {str(e)}")

    extracted_data = []
    seq_counter = 1

    for url, html_content in all_data.items():
        soup = BeautifulSoup(html_content, "html.parser")
        entry = {"seq": seq_counter, "url": url}

        for idx, target in enumerate(targets, 1):
            elements = []
            if target['type'] == 'class':
                elements = soup.find_all(class_=target['name'])
            elif target['type'] == 'id':
                elem = soup.find(id=target['name'])
                if elem: elements = [elem]

            # Combine element texts
            text = " ".join([e.get_text(strip=True) for e in elements if e])

            # Add to entry
            entry[f"{target['type']}{idx}"] = target['name']
            entry[f"text{idx}"] = text

        extracted_data.append(entry)
        seq_counter += 1

    # Save results
    try:
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(extracted_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        raise RuntimeError(f"Failed to save results: {str(e)}")


def extract_data_from_file(filepath, raw_targets):
    """Extract from custom JSON file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            all_data = json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load file: {str(e)}")

    # Parse targets
    try:
        targets = parse_targets(raw_targets)
    except ValueError as e:
        raise RuntimeError(f"Invalid target input: {str(e)}")

    extracted_data = []
    seq_counter = 1

    for url, html_content in all_data.items():
        soup = BeautifulSoup(html_content, "html.parser")
        entry = {"seq": seq_counter, "url": url}

        for idx, target in enumerate(targets, 1):
            elements = []
            if target['type'] == 'class':
                elements = soup.find_all(class_=target['name'])
            elif target['type'] == 'id':
                elem = soup.find(id=target['name'])
                if elem: elements = [elem]

            text = " ".join([e.get_text(strip=True) for e in elements if e])
            entry[f"{target['type']}{idx}"] = target['name']
            entry[f"text{idx}"] = text

        extracted_data.append(entry)
        seq_counter += 1

    output_path = f"{os.path.dirname(filepath)}/extracted_info1.json"
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(extracted_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        raise RuntimeError(f"Failed to save results: {str(e)}")