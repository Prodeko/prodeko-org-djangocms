import React from 'react'
import PropTypes from 'prop-types'

const TableOfContents = ({ sendAnalyticsEvent, content }) => {
  const { data } = content

  const handleClick = (category, header) => {
    sendAnalyticsEvent({
      event: 'tiedoteLinkClicked',
      tiedoteCategory: category,
      tiedoteHeader: header
    })
  }

  return (
    <div id="table-of-contents">
      {data.map((category, key) =>
        category.messages.length > 0 ? (
          <ul key={key} className="main-list">
            <li className="category-title">{category.title}</li>
            <ul className="sub-list">
              {category.messages.map((message, key) => (
                <li key={key} className="message-title">
                  <a
                    href={`#${message.id}`}
                    onClick={() =>
                      handleClick(message.category, message.header)
                    }
                  >
                    {message.header}
                  </a>
                </li>
              ))}
            </ul>
          </ul>
        ) : null
      )}
      <hr />
    </div>
  )
}

TableOfContents.propTypes = {
  content: PropTypes.object.isRequired,
  sendAnalyticsEvent: PropTypes.func.isRequired
}

export default TableOfContents
