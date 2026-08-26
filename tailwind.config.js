import tailwindcssAnimate from 'tailwindcss-animate';

/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ['class'],
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive) / <alpha-value>)',
          foreground: 'hsl(var(--destructive-foreground) / <alpha-value>)',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))',
        },
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
        ceco: {
          bg: '#0D0D0F',
          bg2: '#141418',
          bg3: '#1C1C22',
          text: '#E6E1D8',
          text2: '#8A8580',
          text3: '#6B6560',
          amber: '#C4956A',
          amber2: '#A67C4F',
          green: '#4A7A5C',
          red: '#B85C5C',
          black: '#9A9AA0',
          border: '#2A2A32',
          border2: '#1E1E26',
        },
      },
      fontFamily: {
        display: ['Crimson Pro', 'Georgia', 'serif'],
        body: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      fontSize: {
        'display-xl': ['clamp(3.5rem, 10vw, 9rem)', { lineHeight: '0.9', letterSpacing: '0' }],
        'display-lg': ['clamp(2.5rem, 6vw, 5.5rem)', { lineHeight: '0.95', letterSpacing: '0' }],
        'display-md': ['clamp(1.8rem, 4vw, 3.5rem)', { lineHeight: '1.05', letterSpacing: '0' }],
      },
      boxShadow: {
        glow: '0 0 40px hsl(30 42% 59% / 0.08)',
      },
    },
  },
  plugins: [tailwindcssAnimate],
};
