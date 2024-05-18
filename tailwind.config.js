module.exports = {
  content: [
    './templates/**/*.html',
    './celebritypicker_app/templates/**/*.html',
    './myapp/**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/container-queries'),
  ],
};


