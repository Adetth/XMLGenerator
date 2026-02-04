import xml.etree.ElementTree as ET
import re

#do it one by one, start simple
#future code -  if tag does not exist then create that tag
#               for example, if you have the color tag, and 32768 and 32769 are present
#               and we are trying to add a new color, the code should dynamically add a
#               new color ID with all the parameters

#               Then i have to ensure that that ID is assigned to the row that needs the 
#               color
#               If a form has not been formatted before, create an id for each cell / member
#               and then insert it into the form formatting tag

class XMLModifier:
    def __init__(self):
        self.INPUT_XML_FILE = ""
        self.safe_header = None
        self.tree = None
        self.root = None

    def load_file(self, filepath):
        """Loads the XML file and extracts the safe header block."""
        self.INPUT_XML_FILE = filepath
        self.safe_header = self._extract_header_block(filepath)
        self.tree = ET.parse(filepath)
        self.root = self.tree.getroot()
        print(f"File loaded: {filepath}")

    def _extract_header_block(self, filepath):
        """
        Opens the file as plain text.
        Captures everything from the start of <form...> down to the end of </pipPrefs>.
        Stores it in RAM.
        """
        with open(filepath, "r", encoding="UTF-8") as f:
            content = f.read()

        # Regex Explanation:
        # (?s)      -> Dot matches newline (treat file as one long string)
        # <form     -> Find the literal start of the form tag
        # .*?       -> Match everything in between (non-greedy)
        # </pipPrefs> -> Stop exactly at the closing pipPrefs tag
        pattern = r"(?s)(<form.*?</pipPrefs>)"
        
        match = re.search(pattern, content)
        
        if match:
            print("Header block successfully captured to RAM.")
            return match.group(1) # This is the "Safe" string
        else:
            raise ValueError("Could not find the <form>...<pipPrefs> block in the source file.")

    def _restore_header_block(self):
        """
        Opens the modified (messy) file.
        Finds the SAME block (which is now formatted badly).
        Overwrites it with the 'original_block' from RAM.
        """
        filepath = self.INPUT_XML_FILE
        original_block = self.safe_header

        with open(filepath, "r", encoding="UTF-8") as f:
            new_content = f.read()

        # We use the same pattern to find the "Messy" version in the new file
        pattern = r"(?s)(<form.*?(?:</pipPrefs>|<pipPrefs\s*/>))"
        
        # Check if the pattern exists before trying to replace
        if not re.search(pattern, new_content):
            print("Warning: Could not find the target block in the new file. Replacement skipped.")
            return

        # The Swap: Replace the found 'messy' chunk with the 'clean' original chunk
        final_content = re.sub(pattern, lambda m: original_block, new_content, count=1)
        
        # Write the result back to disk
        with open(filepath, "w", encoding="UTF-8") as f:
            f.write(final_content)
            
        print("Surgical restoration complete: Header formatting restored.")

    def get_colors(self):
        if not self.root:
            return []
            
        color_data = []
        colors = self.root.find(".//values/colors")
        
        if colors is not None:
            for color in colors.findall("color"):
                color_id = color.get("id")
                rgb_values = [color.get("R"), color.get("G"), color.get("B")]
                hex_val = self.rgb_to_hex(rgb_values)
                color_data.append((color_id, hex_val))
            
        return color_data

    def inject_colors(self, color_list):
        if not self.root:
            print("No file loaded.")
            return

        color_map = {str(id_data): color_data for id_data, color_data in color_list}
        colors = self.root.find(".//values/colors")  
         
        updates_made = False
        if colors is not None:
            for color in colors.findall("color"):
                xml_id = str(color.get("id"))
                
                if xml_id in color_map:
                    hex_value = color_map[xml_id]
                    rgb_list = self.hex_to_rgb([hex_value])
                    
                    old_rgb_color = [color.get("R"), color.get("G"), color.get("B")]
                    
                    color.set("R", str(rgb_list[0][0]))
                    color.set("G", str(rgb_list[0][1]))
                    color.set("B", str(rgb_list[0][2]))
                    
                    print(f"Updated ID: {xml_id} from : {old_rgb_color} ==> to : {rgb_list[0]}")
                    updates_made = True

        if updates_made:
            print("Writing changes to file...")
            self.tree.write(self.INPUT_XML_FILE, encoding="UTF-8", xml_declaration=True)
            
            print("Restoring original header formatting...")
            self._restore_header_block()
            print("Done.")
        else:
            print("No matching IDs found. File was not touched.")

    @staticmethod
    def rgb_to_hex(color_list):
        hex_val = f"{int(color_list[0]):02X}{int(color_list[1]):02X}{int(color_list[2]):02X}"
        return hex_val.upper()

    @staticmethod
    def hex_to_rgb(color_list):
        return_color_list = []
        for hex_str in color_list:
            # SAFETY FIX: Remove '#' if present
            clean_hex = hex_str.replace("#", "")
            
            # Now slice the clean string
            r = int(clean_hex[0:2], 16)
            g = int(clean_hex[2:4], 16)
            b = int(clean_hex[4:6], 16)
            
            return_color_list.append([str(r), str(g), str(b)])
        return return_color_list