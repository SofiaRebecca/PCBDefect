import xml.etree.ElementTree as ET
import os

def convert_annotations_to_yolo(input_dir, output_dir, class_names):
    os.makedirs(output_dir, exist_ok=True)
    for category in os.listdir(input_dir):
        category_dir = os.path.join(input_dir, category)
        for xml_file in os.listdir(category_dir):
            if xml_file.endswith(".xml"):
                tree = ET.parse(os.path.join(category_dir, xml_file))
                root = tree.getroot()

                # Image dimensions
                width = int(root.find("size/width").text)
                height = int(root.find("size/height").text)

                yolo_annotations = []
                for obj in root.findall("object"):
                    class_name = obj.find("name").text.strip()  # Strip any leading/trailing spaces

                    # Debugging: Print the class name to verify
                    print(f"Found class in XML: '{class_name}'")

                    # Handle case where class name is not found
                    if class_name not in class_names:
                        print(f"Warning: '{class_name}' not found in class list. Skipping.")
                        continue

                    class_id = class_names.index(class_name)

                    # Bounding box
                    bbox = obj.find("bndbox")
                    xmin = int(bbox.find("xmin").text)
                    ymin = int(bbox.find("ymin").text)
                    xmax = int(bbox.find("xmax").text)
                    ymax = int(bbox.find("ymax").text)

                    # Convert to YOLO format
                    x_center = ((xmin + xmax) / 2) / width
                    y_center = ((ymin + ymax) / 2) / height
                    bbox_width = (xmax - xmin) / width
                    bbox_height = (ymax - ymin) / height
                    yolo_annotations.append(f"{class_id} {x_center} {y_center} {bbox_width} {bbox_height}")

                # Save annotations
                output_path = os.path.join(output_dir, category, xml_file.replace(".xml", ".txt"))
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "w") as f:
                    f.write("\n".join(yolo_annotations))
                    
# Define class names (ensure this list matches the classes in the XML files)
classes = ["spurious_copper", "missing_hole", "mouse_bite", "open_circuit", "short", "spur"]  # Example class names

# Run the conversion
convert_annotations_to_yolo("organized_dataset/train/annotations", "organized_dataset/train/labels", classes)
