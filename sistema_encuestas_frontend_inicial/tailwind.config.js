/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./app/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // Paleta de colores corporativa
        brand: {
          light: '#09B5FF', // rgb(9, 181, 255) - Azul claro
          dark: '#11315B', // rgb(17, 49, 91) - Azul oscuro
          medium: '#2087D5', // rgb(32, 135, 213) - Celeste medio
          vibrant: '#006EBF', // rgb(0, 110, 191) - Azul vibrante
          white: '#FFFFFF', // rgb(255, 255, 255) - Blanco
        },
        // Mantener primary para compatibilidad
        primary: {
          DEFAULT: '#006EBF', // Azul vibrante como principal
          dark: '#11315B', // Azul oscuro
          light: '#09B5FF', // Azul claro
          medium: '#2087D5', // Celeste medio
        },
      },
      fontFamily: { sans: ['Inter', 'sans-serif'] },
    },
  },

  plugins: [],
};
