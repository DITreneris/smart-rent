const React = require('react');
const { render, screen, fireEvent } = require('@testing-library/react');

function customRender(ui, options) {
  return render(ui, options);
}

module.exports = {
  render: customRender,
  screen,
  fireEvent
}; 