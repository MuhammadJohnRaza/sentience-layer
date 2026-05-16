import os

frontend_dir = os.path.join("frontend")
src_dir = os.path.join(frontend_dir, "src")
app_dir = os.path.join(src_dir, "app")
components_dir = os.path.join(src_dir, "components")
hooks_dir = os.path.join(src_dir, "hooks")
lib_dir = os.path.join(src_dir, "lib")

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# package.json
package_json = """{
  "name": "sentience-layer",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "react": "^18",
    "react-dom": "^18",
    "next": "14.2.3",
    "lucide-react": "^0.378.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.1",
    "tailwind-merge": "^2.3.0",
    "@radix-ui/react-slot": "^1.0.2"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "postcss": "^8",
    "tailwindcss": "^3.4.1"
  }
}"""
write_file(os.path.join(frontend_dir, "package.json"), package_json)

# tsconfig.json
tsconfig_json = """{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}"""
write_file(os.path.join(frontend_dir, "tsconfig.json"), tsconfig_json)

# tailwind.config.ts
tailwind_config = """import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
    },
  },
  plugins: [],
};
export default config;"""
write_file(os.path.join(frontend_dir, "tailwind.config.ts"), tailwind_config)

# postcss.config.mjs
postcss_config = """/** @type {import('postcss-load-config').Config} */
const config = {
  plugins: {
    tailwindcss: {},
  },
};
export default config;"""
write_file(os.path.join(frontend_dir, "postcss.config.mjs"), postcss_config)

# globals.css
globals_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: #ffffff;
  --foreground: #171717;
}

@media (prefers-color-scheme: dark) {
  :root {
    --background: #0a0a0a;
    --foreground: #ededed;
  }
}

body {
  color: var(--foreground);
  background: var(--background);
  font-family: Arial, Helvetica, sans-serif;
}
"""
write_file(os.path.join(src_dir, "app", "globals.css"), globals_css)

# layout.tsx
layout_tsx = """import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Sentience Layer",
  description: "Autonomous Agent System",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}"""
write_file(os.path.join(app_dir, "layout.tsx"), layout_tsx)

# page.tsx
page_tsx = """import { ChatInterface } from "@/components/chat/ChatInterface";

export default function Home() {
  return (
    <main className="flex h-screen w-full flex-col items-center justify-between bg-gray-50">
      <div className="w-full max-w-5xl h-full shadow-xl bg-white">
        <ChatInterface />
      </div>
    </main>
  );
}"""
write_file(os.path.join(app_dir, "page.tsx"), page_tsx)

# lib/utils.ts
utils_ts = """import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}"""
write_file(os.path.join(lib_dir, "utils.ts"), utils_ts)

# hooks/useChat.ts
use_chat_ts = """import { useState } from 'react';

export function useChat() {
  const sendMessage = async (message: string) => {
    return new Promise<any>((resolve) => {
      setTimeout(() => {
        resolve({
          insight: { title: "Insight derived", description: "This is a placeholder insight based on: " + message },
        });
      }, 1000);
    });
  };
  return { sendMessage };
}"""
write_file(os.path.join(hooks_dir, "useChat.ts"), use_chat_ts)

# hooks/useMediaQuery.ts
use_media_query_ts = """import { useState, useEffect } from 'react';

export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    if (media.matches !== matches) {
      setMatches(media.matches);
    }
    const listener = () => setMatches(media.matches);
    media.addEventListener('change', listener);
    return () => media.removeEventListener('change', listener);
  }, [matches, query]);

  return matches;
}"""
write_file(os.path.join(hooks_dir, "useMediaQuery.ts"), use_media_query_ts)

# Components stubs
components_to_create = {
    "InsightCard.tsx": """export function InsightCard({ insight }: { insight: any }) { return <div className="p-4 border rounded-lg bg-blue-50 text-blue-900"><strong>Insight:</strong> {insight?.title || 'No Title'} <p>{insight?.description}</p></div>; }""",
    "ActionPanel.tsx": """export function ActionPanel({ actions }: { actions: any }) { return <div className="p-4 border rounded-lg bg-green-50 text-green-900">Action Panel</div>; }""",
    "SimulationDashboard.tsx": """export function SimulationDashboard({ simulation }: { simulation: any }) { return <div className="p-4 border rounded-lg bg-purple-50 text-purple-900">Simulation Dashboard</div>; }""",
    "AgentTraceViewer.tsx": """export function AgentTraceViewer({ traces }: { traces: any }) { return <div className="p-4 border rounded-lg bg-gray-50 text-gray-900 font-mono text-xs">Agent Trace Viewer</div>; }""",
    "ActionLogger.tsx": """export function ActionLogger() { return <div>Action Logger Component</div>; }"""
}
for name, content in components_to_create.items():
    write_file(os.path.join(components_dir, "chat" if name != "ActionLogger.tsx" else "ActionLogger", name), content)
write_file(os.path.join(components_dir, "ActionLogger.tsx"), components_to_create["ActionLogger.tsx"])

# App page stubs
pages = [
    "causal-explorer", "dashboard", "doubt-room", "dreamscape", "economic-model",
    "memory", "mirror", "mission-control", "playbook", "simulate", "trace", "vault", "win"
]
for p in pages:
    content = f'''export default function {p.replace("-", "").capitalize()}Page() {{
  return (
    <div className="flex h-full flex-col bg-white p-6">
      <h1 className="mb-6 text-2xl font-semibold text-gray-900">{p.replace("-", " ").title()}</h1>
      <p>This page is currently under construction.</p>
    </div>
  );
}}'''
    write_file(os.path.join(app_dir, p, "page.tsx"), content)

print("Scaffold completed successfully.")
