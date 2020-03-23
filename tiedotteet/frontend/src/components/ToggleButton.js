import React from 'react'
import PropTypes from 'prop-types'

const ToggleButton = ({ handleClick, show }) =>
  !show ? null : <div className="toggle-button" onClick={handleClick} />

ToggleButton.propTypes = {
  show: PropTypes.bool.isRequired,
  handleClick: PropTypes.func.isRequired,
}

export default ToggleButton
