import React, { Component } from 'react'
import PropTypes from 'prop-types'

class ScrollControl extends Component {
  render() {
    return (
      <div id="scroll-control" className="control-button" onClick={this.props.handleClick}>
        <i className="fa fa-arrow-up"></i>
      </div>
    )
  }
}

ScrollControl.propTypes = {
  handleClick: PropTypes.func.isRequired
}

export default ScrollControl
