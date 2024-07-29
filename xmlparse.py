import xml.etree.ElementTree as ET
import sys

def update_plant_price(xml_file, plant_name, percent_change):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Find all plants
    plants = root.findall('PLANT')
    
    # Flag to check if the plant was found
    plant_found = False
    
    # Loop through each plant to find the matching name
    for plant in plants:
        common_name = plant.find('COMMON').text
        
        if common_name == plant_name:
            # Check if the price is already updated
            updated_elem = plant.find('UPDATED')
            if updated_elem is not None and updated_elem.text == 'true':
                print(f"Price for '{plant_name}' has already been updated.")
                return
            
            # Get the current price
            price_elem = plant.find('PRICE')
            current_price = float(price_elem.text)
            
            # Calculate the new price
            new_price = current_price * (1 + percent_change / 100)
            
            # Update the price element with the new price
            price_elem.text = f"{new_price:.2f}"
            
            # Mark this plant as updated
            if updated_elem is None:
                updated_elem = ET.SubElement(plant, 'UPDATED')
            updated_elem.text = 'true'
            
            # Save the modified XML to a new file
            tree.write('updated_plant_catalog.xml', encoding='utf-8', xml_declaration=True)
            print(f"Updated price for '{plant_name}' to {new_price:.2f}")
            
            plant_found = True
            break
    
    if not plant_found:
        print(f"Plant named '{plant_name}' not found.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python xmlparse.py plant_catalog.xml plantName percentChange")
        sys.exit(1)
    
    xml_file = sys.argv[1]
    plant_name = sys.argv[2]
    percent_change = float(sys.argv[3])
    
    update_plant_price(xml_file, plant_name, percent_change)
