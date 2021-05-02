const colors = require('tailwindcss/colors')
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  purge: { content: ['./public/**/*.html', './src/**/*.vue'] },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      container: {
        padding: '1rem'
      },
      width: {
        '1/7': '14.2857143%',
      },
      spacing: {
        '13': '3.25rem',
        '15': '3.75rem',
        '128': '32rem',
        '144': '36rem',
        '168': '42rem',
        '728px': '728px'
      },
      inset: {
        '110px': '110px',
      },
      colors: { 
        gray: colors.trueGray
      },
      fontFamily: {
        sans: ['Quicksand', ...defaultTheme.fontFamily.sans],
      },
      gridTemplateRows: {
       '7': 'repeat(7, minmax(0, 1fr))',
      }
    },
    screens: {
      sm: '576px',
      md: '768px',
      lg: '992px',
      xl: '1200px',
    },
    backgroundPosition: {
      'center-center': 'center center',
      '-top-32': 'center top -8rem',
    },
    objectPosition: {
     'center-hero': ' 0% 8%',
    }
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
