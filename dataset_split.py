import os
import shutil
from sklearn.model_selection import train_test_split

def organize_dataset(base_dir, output_dir, split_ratio=(0.8, 0.1, 0.1)):
    categories = os.listdir(os.path.join(base_dir, "images"))
    for category in categories:
        img_dir = os.path.join(base_dir, "images", category)
        ann_dir = os.path.join(base_dir, "annotations", category)
        images = os.listdir(img_dir)

        train, temp = train_test_split(images, test_size=1 - split_ratio[0], random_state=42)
        val, test = train_test_split(temp, test_size=split_ratio[2] / (split_ratio[1] + split_ratio[2]), random_state=42)

        for split, subset in zip(["train", "val", "test"], [train, val, test]):
            split_img_dir = os.path.join(output_dir, split, "images", category)
            split_ann_dir = os.path.join(output_dir, split, "annotations", category)
            os.makedirs(split_img_dir, exist_ok=True)
            os.makedirs(split_ann_dir, exist_ok=True)
            
            for img_file in subset:
                shutil.copy(os.path.join(img_dir, img_file), os.path.join(split_img_dir, img_file))
                xml_file = img_file.replace(".jpg", ".xml")
                shutil.copy(os.path.join(ann_dir, xml_file), os.path.join(split_ann_dir, xml_file))

# Organize the dataset
organize_dataset("PCB_DATASET", "organized_dataset")