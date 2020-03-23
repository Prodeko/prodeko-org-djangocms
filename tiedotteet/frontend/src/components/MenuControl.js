import React from 'react'
import PropTypes from 'prop-types'

const MenuControl = ({ handleClick }) => (
  <div id="menu-control" className="control-button" onClick={handleClick}>
    <i className="fas fa-bars" />
  </div>
)

MenuControl.propTypes = {
  handleClick: PropTypes.func.isRequired,
}

export default MenuControl
