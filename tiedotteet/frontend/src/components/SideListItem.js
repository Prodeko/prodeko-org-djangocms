import React from 'react'
import PropTypes from 'prop-types'
import Moment from 'moment'
import { isInStore } from '../util/localStorage'

const SideListItem = ({ sendAnalyticsEvent, message }) => {
  const handleClick = () => {
    sendAnalyticsEvent({
      event: 'tiedoteLinkClicked',
      tiedoteCategory: message.category,
      tiedoteHeader: message.header
    })
  }

  return (
    <li
      className={`sidebar-list-item ${isInStore(message.id) ? 'read' : ''} ${
        message.isNew ? 'new' : ''
      }`}
    >
      <a htmlFor={message.id} href={`#${message.id}`} onClick={handleClick}>
        {message.is_new && (
          <div className="icon-container text-red">
            <span>New</span>
          </div>
        )}
        {message.show_deadline && (
          <div className="icon-container text-light-grey">
            <span>DL: {Moment(message.deadline_date).format('D.M.Y')}</span>
          </div>
        )}
        <div className="text-container">{message.header}</div>
      </a>
    </li>
  )
}

SideListItem.propTypes = {
  message: PropTypes.object.isRequired,
  sendAnalyticsEvent: PropTypes.func.isRequired
}

export default SideListItem
