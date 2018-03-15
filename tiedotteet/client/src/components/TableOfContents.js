import React, { Component } from 'react'
import PropTypes from 'prop-types'

class TableOfContents extends Component {

  handleClick = (messageHeader, messageIsNew) => {
    this.props.sendAnalyticsEvent('table of contents link', 'click', messageHeader, messageIsNew ? 1 : 0)
  }

  render() {
    return (
      <div id="table-of-contents">
        {this.props.content.data.map((category, key) =>  category.messages.length > 0 ? (
          <ul key={key} className="main-list">
            <li className="category-title">{category.title}</li>
            <ul className="sub-list">
              {category.messages.map((message, key) => (
                <li key={key} className="message-title">
                  <a href={`#${message.id}`} onClick={() => this.handleClick(message.header, message.isNew)}>{message.header}</a>
                </li>
              ))}
            </ul>
          </ul>

        ) : null)}
        <hr/>
      </div>
    )
  }
}

TableOfContents.propTypes = {
  content: PropTypes.object.isRequired,
  sendAnalyticsEvent: PropTypes.func.isRequired
}

export default TableOfContents