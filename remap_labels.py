"""
Script to remap YOLO label files to match the current YAML class order.

Current YAML order:
  0: Player
  1: Cone
  2: Coin
  3: Hole
  4: Plane
  5: Roadblock
  6: Ball

Original label files order (from classes.txt):
  0: Player
  1: Plane
  2: Roadblock
  3: Coin
  4: Cone
  5: Ball
  6: Hole

Mapping: old_index -> new_index
"""
import os
from pathlib import Path

# Define the mapping from old class indices to new class indices
# Based on: old_classes.txt order -> new YAML order
OLD_TO_NEW_MAPPING = {
    0: 0,  # Player stays the same
    1: 4,  # Plane: 1 -> 4
    2: 5,  # Roadblock: 2 -> 5
    3: 2,  # Coin: 3 -> 2
    4: 1,  # Cone: 4 -> 1
    5: 6,  # Ball: 5 -> 6
    6: 3,  # Hole: 6 -> 3
    7: 3,  # Class 7 (likely error, mapping to Hole)
}

def remap_label_file(label_path):
    """Remap class indices in a single label file."""
    try:
        with open(label_path, 'r') as f:
            lines = f.readlines()
        
        remapped_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                remapped_lines.append('')
                continue
            
            parts = line.split()
            if len(parts) >= 5:
                old_class = int(parts[0])
                if old_class in OLD_TO_NEW_MAPPING:
                    new_class = OLD_TO_NEW_MAPPING[old_class]
                    new_line = f"{new_class} {' '.join(parts[1:])}\n"
                    remapped_lines.append(new_line)
                else:
                    print(f"Warning: Unknown class {old_class} in {label_path}, keeping as is")
                    remapped_lines.append(line + '\n')
            else:
                remapped_lines.append(line + '\n')
        
        with open(label_path, 'w') as f:
            f.writelines(remapped_lines)
        
        return True
    except Exception as e:
        print(f"Error processing {label_path}: {e}")
        return False

def main():
    dataset_path = Path("datasets/NeckDeep")
    train_labels_dir = dataset_path / "labels" / "train"
    val_labels_dir = dataset_path / "labels" / "val"
    
    print("Remapping label files to match YAML class order...")
    print(f"Mapping: {OLD_TO_NEW_MAPPING}\n")
    
    # Process train labels
    train_files = list(train_labels_dir.glob("*.txt"))
    train_files = [f for f in train_files if f.name != "classes.txt"]
    
    print(f"Processing {len(train_files)} training label files...")
    train_success = 0
    for label_file in train_files:
        if remap_label_file(label_file):
            train_success += 1
    
    # Process val labels
    val_files = list(val_labels_dir.glob("*.txt"))
    val_files = [f for f in val_files if f.name != "classes.txt"]
    
    print(f"Processing {len(val_files)} validation label files...")
    val_success = 0
    for label_file in val_files:
        if remap_label_file(label_file):
            val_success += 1
    
    print(f"\nDone!")
    print(f"Train: {train_success}/{len(train_files)} files remapped")
    print(f"Val: {val_success}/{len(val_files)} files remapped")
    
    # Update classes.txt to match YAML
    print("\nUpdating classes.txt files to match YAML...")
    new_classes = ["Player", "Cone", "Coin", "Hole", "Plane", "Roadblock", "Ball"]
    
    for classes_file in [train_labels_dir / "classes.txt", val_labels_dir / "classes.txt"]:
        if classes_file.exists():
            with open(classes_file, 'w') as f:
                f.write('\n'.join(new_classes) + '\n')
            print(f"Updated {classes_file}")

if __name__ == "__main__":
    main()

