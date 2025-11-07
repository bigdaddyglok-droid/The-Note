import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "#06070f",
        surface: "#111326",
        accent: "#5b8def",
        success: "#2dd197",
        warning: "#ffb648",
        danger: "#ff5f5f"
      },
      fontFamily: {
        sans: ["'Inter var'", "system-ui", "sans-serif"],
        mono: ["'IBM Plex Mono'", "monospace"]
      },
      boxShadow: {
        focus: "0 0 0 3px rgba(91, 141, 239, 0.45)"
      }
    }
  },
  plugins: []
};

export default config;
