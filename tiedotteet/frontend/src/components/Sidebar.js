import React from 'react'
import PropTypes from 'prop-types'
import SideListItem from './SideListItem'

const Sidebar = props => {
  const { additionalClasses, sendAnalyticsEvent, content } = props

  return (
    <aside id="sidebar" className={additionalClasses}>
      <div id="sidebar-content">
        {content.data
          .filter(c => c.messages.length > 0)
          .map((d, key) => (
            <div key={key}>
              <span className="sidebar-category">{d.title}</span>
              <ul className="sidebar-list">
                {d.messages.map((m, key) => (
                  <SideListItem
                    key={key}
                    message={m}
                    sendAnalyticsEvent={sendAnalyticsEvent}
                  />
                ))}
              </ul>
            </div>
          ))}
      </div>
    </aside>
  )
}

Sidebar.propTypes = {
  content: PropTypes.object.isRequired,
  markRead: PropTypes.func.isRequired,
  markUnread: PropTypes.func.isRequired,
  additionalClasses: PropTypes.string,
  sendAnalyticsEvent: PropTypes.func.isRequired
}

export default Sidebar
