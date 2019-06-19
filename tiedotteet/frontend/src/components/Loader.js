import React, { Component } from "react";

class Loader extends Component {
  render() {
    return (
      <div className="loader">
        <img src="/static/assets/prodeko.png" alt="Loading..." />
      </div>
    );
  }
}

Loader.propTypes = {};

export default Loader;
