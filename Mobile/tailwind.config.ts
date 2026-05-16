import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        neon: {
          red: "#FF0040",
          orange: "#FF6B00",
          amber: "#FFB800",
          pink: "#FF0080",
        },
        cyber: {
          dark: "#0a0a0f",
          darker: "#050508",
          gray: "#1a1a24",
          border: "#2a2a3a",
        },
      },
      boxShadow: {
        neon: "0 0 20px rgba(255, 0, 64, 0.5), 0 0 40px rgba(255, 0, 64, 0.3)",
        "neon-orange": "0 0 20px rgba(255, 107, 0, 0.5), 0 0 40px rgba(255, 107, 0, 0.3)",
        "neon-amber": "0 0 20px rgba(255, 184, 0, 0.5), 0 0 40px rgba(255, 184, 0, 0.3)",
        glow: "0 0 30px rgba(255, 0, 64, 0.6), 0 0 60px rgba(255, 107, 0, 0.4)",
      },
      animation: {
        glow: "glow 2s ease-in-out infinite alternate",
        pulse: "pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        float: "float 3s ease-in-out infinite",
      },
      keyframes: {
        glow: {
          "0%": { boxShadow: "0 0 20px rgba(255, 0, 64, 0.5), 0 0 40px rgba(255, 0, 64, 0.3)" },
          "100%": { boxShadow: "0 0 30px rgba(255, 107, 0, 0.6), 0 0 60px rgba(255, 107, 0, 0.4)" },
        },
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-10px)" },
        },
      },
      backdropBlur: {
        xs: "2px",
      },
    },
  },
  plugins: [],
};

export default config;
