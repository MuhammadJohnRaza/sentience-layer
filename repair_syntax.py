import os
import re

def repair_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # If it has newlines, it might not be the mangled one.
    if content.count('\n') > 5:
        return

    # Add newlines before common keywords that start a statement
    keywords = ["import ", "export ", "const ", "let ", "var ", "function ", "return ", "interface ", "type ", "class ", "if ", "for ", "while ", "switch ", "try ", "catch "]
    
    repaired = content
    for kw in keywords:
        repaired = repaired.replace(f" {kw}", f"\n{kw}")
    
    # Fix ending braces
    repaired = repaired.replace("} export", "}\nexport")
    repaired = repaired.replace("} const", "}\nconst")
    repaired = repaired.replace("} function", "}\nfunction")
    repaired = repaired.replace("; ", ";\n")
    repaired = repaired.replace("} ", "}\n")
    repaired = repaired.replace("{ ", "{\n")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(repaired)
    print(f"Repaired {filepath}")

directories = [
    r"c:\Users\catac\OneDrive\Desktop\sentience-layer\frontend\src",
    r"c:\Users\catac\OneDrive\Desktop\sentience-layer\mobile\src"
]

for d in directories:
    if not os.path.exists(d):
        continue
    for root, _, files in os.walk(d):
        for file in files:
            if file.endswith(('.tsx', '.ts', '.js', '.jsx')):
                repair_file(os.path.join(root, file))

print("Syntax repair complete.")
