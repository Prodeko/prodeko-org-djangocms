import React, { Component } from 'react'
import PropTypes from 'prop-types'

class ToggleButton extends Component {
  render() {
    if (!this.props.show) {
      return null
    }
    return (
      <div className="toggle-button" onClick={this.props.handleClick}></div>
    )
  }
}

ToggleButton.propTypes = {
  show: PropTypes.bool.isRequired,
  handleClick: PropTypes.func.isRequired
}

export default ToggleButton
