import React, { Component } from 'react'
import PropTypes from 'prop-types'

class Loader extends Component {
  render() {
    return (
      <div className="loader">
        <img src={"/public/assets/prodeko.png"} alt="Loading..."/>
      </div>
    )
  }
}

Loader.propTypes = {

}

export default Loader
