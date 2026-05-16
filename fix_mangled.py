import os

broken_files = [
    r"c:\Users\catac\OneDrive\Desktop\sentience-layer\frontend\src\components\ui\button.tsx",
    r"c:\Users\catac\OneDrive\Desktop\sentience-layer\frontend\src\components\ui\card.tsx",
    r"c:\Users\catac\OneDrive\Desktop\sentience-layer\frontend\src\components\ui\input.tsx",
    r"c:\Users\catac\OneDrive\Desktop\sentience-layer\frontend\src\hooks\useAgentTraces.ts",
    r"c:\Users\catac\OneDrive\Desktop\sentience-layer\frontend\src\lib\api.ts",
    r"c:\Users\catac\OneDrive\Desktop\sentience-layer\mobile\src\hooks\useOfflineSync.ts",
    r"c:\Users\catac\OneDrive\Desktop\sentience-layer\mobile\src\screens\AgentTraceScreen.js",
    r"c:\Users\catac\OneDrive\Desktop\sentience-layer\mobile\src\screens\MemoryScreen.js",
    r"c:\Users\catac\OneDrive\Desktop\sentience-layer\mobile\src\screens\SettingsScreen.js",
    r"c:\Users\catac\OneDrive\Desktop\sentience-layer\mobile\src\services\api.ts",
    r"c:\Users\catac\OneDrive\Desktop\sentience-layer\mobile\src\services\sync.ts",
    r"c:\Users\catac\OneDrive\Desktop\sentience-layer\mobile\src\store\workflowSlice.js",
    r"c:\Users\catac\OneDrive\Desktop\sentience-layer\mobile\src\utils\constants.ts",
    r"c:\Users\catac\OneDrive\Desktop\sentience-layer\mobile\src\utils\helpers.ts",
]

for filepath in broken_files:
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix unterminated strings / bad newlines before "for "
    content = content.replace("\nfor ", " for ")
    
    # Fix broken export/import in button.tsx etc
    content = content.replace(") Button.displayName =\"Button\"", ")\nButton.displayName = \"Button\"")
    content = content.replace(") Card.displayName =\"Card\"", ")\nCard.displayName = \"Card\"")
    content = content.replace(") Input.displayName =\"Input\"", ")\nInput.displayName = \"Input\"")
    
    # Fix frontend/src/hooks/useAgentTraces.ts: SyntaxError: Declaration or statement expected.
    content = content.replace("}, []);\nconst", "}, []);\n\nconst")
    
    # Fix frontend/src/lib/api.ts
    content = content.replace("}), getChatHistory:", "}),\ngetChatHistory:")
    content = content.replace("}), // Insights getInsights:", "}),\n// Insights\ngetInsights:")
    content = content.replace("}), // Actions getActions:", "}),\n// Actions\ngetActions:")
    content = content.replace("}), simulateAction:", "}),\nsimulateAction:")
    content = content.replace("}), // Agents getAgentTraces:", "}),\n// Agents\ngetAgentTraces:")
    content = content.replace("}), getAgentStatus:", "}),\ngetAgentStatus:")
    content = content.replace("}), // Memory getMemory:", "}),\n// Memory\ngetMemory:")
    content = content.replace("\")), searchMemory:", "\")),\nsearchMemory:")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Fixed specific broken files.")
