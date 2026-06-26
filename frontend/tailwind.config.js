/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,jsx}',
  ],
  theme: {
    extend: {
      colors: {
        swiss: {
          white: '#FFFFFF',
          black: '#000000',
          gray: '#F2F2F2',
          red: '#FF3000'
        }
      },
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
      },
      backgroundImage: {
        'swiss-grid': 'linear-gradient(to right, rgba(0,0,0,0.05) 1px, transparent 1px), linear-gradient(to bottom, rgba(0,0,0,0.05) 1px, transparent 1px)',
        'swiss-dots': 'radial-gradient(circle, rgba(0,0,0,0.08) 1.5px, transparent 1.5px)',
        'swiss-diagonal': 'repeating-linear-gradient(45deg, rgba(0,0,0,0.03), rgba(0,0,0,0.03) 2px, transparent 2px, transparent 10px)',
      },
      backgroundSize: {
        'swiss-grid': '24px 24px',
        'swiss-dots': '16px 16px',
      }
    },
  },
  plugins: [],
}
