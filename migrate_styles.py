import os
import re

directories = [
    r"c:\Users\catac\OneDrive\Desktop\sentience-layer\frontend\src",
    r"c:\Users\catac\OneDrive\Desktop\sentience-layer\mobile\src"
]

replacements = {
    r"bg-slate-950": "bg-background",
    r"bg-slate-900": "bg-card",
    r"bg-slate-800": "bg-border/30",
    r"bg-slate-100": "bg-border/10",
    r"bg-slate-50": "bg-background",
    r"border-slate-800": "border-border",
    r"border-slate-700": "border-border",
    r"border-slate-200": "border-border",
    r"text-slate-50": "text-foreground",
    r"text-slate-400": "text-muted-foreground",
    r"text-slate-500": "text-muted-foreground",
    r"text-slate-900": "text-foreground",
    r"text-zinc-900": "text-foreground",
    r"text-zinc-800": "text-foreground",
    r"text-zinc-700": "text-muted-foreground",
    r"text-zinc-600": "text-muted-foreground",
    r"text-zinc-500": "text-muted-foreground",
    r"bg-zinc-900": "bg-card",
    r"bg-zinc-800": "bg-border/30",
    r"border-zinc-800": "border-border",
    r"border-zinc-700": "border-border",
    r"dark:bg-slate-950": "",
    r"dark:bg-slate-900": "",
    r"dark:border-slate-800": "",
    r"dark:text-slate-50": "",
    r"dark:text-slate-400": "",
    r"bg-emerald-500": "bg-primary",
    r"bg-red-500": "bg-destructive",
    r"text-emerald-500": "text-primary-foreground",
    r"text-red-500": "text-destructive-foreground",
    r"bg-blue-600": "bg-primary",
    r"bg-blue-500": "bg-primary",
    r"bg-indigo-600": "bg-primary",
    r"text-indigo-400": "text-primary-foreground",
    r"text-[#EAB308]": "text-primary-foreground",
    r"bg-[#A855F7]": "bg-accent",
    r"text-[#A855F7]": "text-accent-foreground",
    r"bg-[#EAB308]": "bg-primary-foreground",
    r"fill=\"#A855F7\"": "fill=\"hsl(var(--accent))\"",
    r"stroke=\"#A855F7\"": "stroke=\"hsl(var(--accent))\"",
    r"fill=\"#EAB308\"": "fill=\"hsl(var(--primary-foreground))\"",
    r"stroke=\"#EAB308\"": "stroke=\"hsl(var(--primary-foreground))\"",
    r"border-zinc-900/40": "border-border/40",
    r"bg-zinc-900/40": "bg-card/40"
}

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    for old, new in replacements.items():
        new_content = new_content.replace(old, new)
        
    # Extra cleanup for extra spaces left from dark: classes removal
    new_content = re.sub(r'\s+', ' ', new_content).replace('className=" ', 'className="').replace(' "', '"')

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for d in directories:
    if not os.path.exists(d):
        continue
    for root, _, files in os.walk(d):
        for file in files:
            if file.endswith(('.tsx', '.ts', '.js', '.jsx')):
                process_file(os.path.join(root, file))

print("Style migration complete.")
