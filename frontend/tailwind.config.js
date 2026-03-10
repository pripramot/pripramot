/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'forensic-blue': '#0a192f',
        'forensic-teal': '#64ffda',
        'forensic-gray': '#8892b0',
      },
      backdropBlur: {
        xs: '2px',
      }
    },
  },
  plugins: [],
}
