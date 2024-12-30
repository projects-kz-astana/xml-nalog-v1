import pandas as pd
from lxml import etree
from datetime import datetime

def create_xml_from_excel(excel_file, output_xml_file):
    # Read Excel file
    df = pd.read_excel(excel_file)
    
    # Create parser with remove_blank_text to allow for pretty printing
    parser = etree.XMLParser(remove_blank_text=True)
    
    # Create root element with proper namespace handling
    NSMAP = {
        'xs': 'http://www.w3.org/2001/XMLSchema',
        'fn': 'http://www.w3.org/2005/xpath-functions',
        'ds': 'http://www.w3.org/2000/09/xmldsig#'
    }
    root = etree.Element("fno", nsmap=NSMAP,
                        attrib={
                            "code": "270.00",
                            "formatVersion": "1",
                            "version": "2"
                        })

    current_form = None
    current_sheet = None
    current_sheet_group = None

    # Process each row in the Excel file
    for _, row in df.iterrows():
        form_name = str(row.get('form', '')).strip()
        sheet_name = str(row.get('sheet', '')).strip()
        field_name = str(row.get('field', '')).strip()
        
        # Convert value to string, handling NaN and special cases
        value = row.get('value', '')
        if pd.isna(value):
            value = None  # This will create self-closing tags
        elif isinstance(value, bool):
            value = str(value).lower()
        elif isinstance(value, (int, float)):
            # Remove .0 from integer values
            if float(value).is_integer():
                value = str(int(value))
            else:
                value = str(value)
        else:
            value = str(value)

        # Skip empty rows
        if not form_name or not sheet_name or not field_name:
            continue

        # Find or create form element
        if current_form is None or current_form.get('name') != form_name:
            form_elem = root.find(f".//form[@name='{form_name}']")
            if form_elem is None:
                form_elem = etree.SubElement(root, "form", name=form_name)
                sheet_group = etree.SubElement(form_elem, "sheetGroup")
                current_form = form_elem
                current_sheet_group = sheet_group
            else:
                current_form = form_elem
                current_sheet_group = form_elem.find("sheetGroup")

        # Find or create sheet element
        if current_sheet is None or current_sheet.get('name') != sheet_name:
            sheet_elem = current_sheet_group.find(f"./sheet[@name='{sheet_name}']")
            if sheet_elem is None:
                sheet_elem = etree.SubElement(current_sheet_group, "sheet", name=sheet_name)
            current_sheet = sheet_elem

        # Create field element
        field_elem = etree.SubElement(current_sheet, "field", name=field_name)
        if value is not None:  # Only set text if value is not None
            field_elem.text = value

    # Custom XML declaration
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    
    # Convert to string with custom formatting
    xml_string = etree.tostring(root, encoding='UTF-8', pretty_print=True, xml_declaration=False)
    
    # Decode bytes to string, split into lines
    xml_lines = xml_string.decode('UTF-8').split('\n')
    
    # Add proper indentation to root element attributes
    root_lines = xml_lines[0].split(' xmlns:')
    formatted_root = root_lines[0] + '\n'
    for i, ns in enumerate(root_lines[1:], 1):
        if i < len(root_lines[1:]):
            formatted_root += '     xmlns:' + ns + '\n'
        else:
            # For the last namespace line, split off the attributes
            ns_parts = ns.split(' code=')
            formatted_root += '     xmlns:' + ns_parts[0] + '\n'
            formatted_root += '     code=' + 'code='.join(ns_parts[1:])
    xml_lines[0] = formatted_root.rstrip()
    
    # Join back together
    formatted_xml = xml_declaration + '\n'.join(xml_lines)
    
    # Write to file
    with open(output_xml_file, 'w', encoding='UTF-8') as f:
        f.write(formatted_xml)

if __name__ == "__main__":
    excel_file = "new_excel_xml.xlsx"
    output_xml_file = "generated_from_new.xml"
    create_xml_from_excel(excel_file, output_xml_file)
