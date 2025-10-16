/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#4F46E5',
        severity: {
          critical: '#DC2626',
          high: '#EA580C',
          medium: '#F59E0B',
          low: '#10B981',
          info: '#3B82F6',
        },
        status: {
          queued: '#6B7280',
          running: '#3B82F6',
          completed: '#10B981',
          failed: '#DC2626',
        }
      },
    },
  },
  plugins: [],
}
