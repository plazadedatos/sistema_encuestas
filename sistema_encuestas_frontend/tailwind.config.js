/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
  extend: {
    colors: {
      primary: { DEFAULT: "#0057B8", dark: "#003E85", light: "#4c8de0" },
    },
    fontFamily: { sans: ["Inter", "sans-serif"] },
  },
},

  plugins: [],
};
