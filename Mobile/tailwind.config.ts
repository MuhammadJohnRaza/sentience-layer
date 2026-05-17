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
          red: "#7C3AED",     // Glowing Purple
          orange: "#A855F7",  // Vibrant Violet
          amber: "#FCD34D",   // Lustrous Gold
          pink: "#C084FC",    // Light Purple
        },
        cyber: {
          dark: "#050508",
          darker: "#000000",
          gray: "#0b0b10",
          border: "#7c3aed",
        },
      },
      boxShadow: {
        neon: "0 0 20px rgba(124, 58, 237, 0.5), 0 0 40px rgba(124, 58, 237, 0.3)",
        "neon-orange": "0 0 20px rgba(168, 85, 247, 0.5), 0 0 40px rgba(168, 85, 247, 0.3)",
        "neon-amber": "0 0 20px rgba(252, 211, 77, 0.5), 0 0 40px rgba(252, 211, 77, 0.3)",
        glow: "0 0 30px rgba(124, 58, 237, 0.6), 0 0 60px rgba(168, 85, 247, 0.4)",
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
