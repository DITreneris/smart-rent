/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Poppins", "ui-sans-serif", "system-ui", "-apple-system"],
        body: ["Roboto", "ui-sans-serif", "system-ui", "-apple-system"],
      },
      colors: {
        primary: "#1A73E8",
        accent: "#2D9CDB",
        "neutral-900": "#1F2937",
        "neutral-100": "#F9FAFB",
        "card-bg": "#FFFFFF",
        "secondary-text": "#4B5563",
        success: "#10B981",
        danger: "#EF4444",
      },
      boxShadow: {
        card: "0 2px 8px rgba(0, 0, 0, 0.05)",
        hover: "0 4px 12px rgba(0, 0, 0, 0.1)",
      },
      transitionTimingFunction: {
        "in-out": "cubic-bezier(0.4, 0, 0.2, 1)",
      },
      spacing: {
        section: "5rem",
        "card-gap": "2rem",
      },
      borderRadius: {
        lg: "1rem",
        xl: "1.5rem",
      },
      fontSize: {
        hero: "2.75rem",
        subheadline: "1.25rem",
      },
    },
  },
  plugins: [],
} 