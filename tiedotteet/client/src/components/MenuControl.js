import React, { Component } from 'react'
import PropTypes from 'prop-types'

class MenuControl extends Component {
  render() {
    return (
      <div
        id={`menu-control`}
        className="control-button"
        onClick={this.props.handleClick}
      >
        <i className="fa fa-bars"></i>
      </div>
    )
  }
}

MenuControl.propTypes = {
  handleClick: PropTypes.func.isRequired
}

export default MenuControl
