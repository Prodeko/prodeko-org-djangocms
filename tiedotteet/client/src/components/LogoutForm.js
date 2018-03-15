import React, { Component } from 'react'
import PropTypes from 'prop-types'

class LogoutForm extends Component {
  render() {
    return (
      <div className="auth-form">
        <form method="get" action="/logout/">
          <div className="user-text">{window.user}</div>
          <input type="hidden" name="next" value="/"/>
          <button type="submit">Logout</button>
        </form>
      </div>
    )
  }
}

LogoutForm.propTypes = {
}

export default LogoutForm
