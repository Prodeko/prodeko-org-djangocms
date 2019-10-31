import React from 'react'
import PropTypes from 'prop-types'

const ScrollControl = ({ handleClick }) => (
  <div id="scroll-control" className="control-button" onClick={handleClick}>
    <i className="fas fa-arrow-up" />
  </div>
)

ScrollControl.propTypes = {
  handleClick: PropTypes.func.isRequired
}

export default ScrollControl
