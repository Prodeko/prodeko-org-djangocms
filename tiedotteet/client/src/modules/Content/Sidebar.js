import React, { Component } from 'react'
import PropTypes from 'prop-types'
import SideListItem from '../../components/SideListItem'

class Sidebar extends Component {
  render() {
    return (
      <aside id="sidebar" className={this.props.additionalClasses}>
        <div id="sidebar-content">
        {this.props.content.data.filter(c => c.messages.length > 0).map((d, key) => (
          <div key={key}>
            <span className="sidebar-category">{d.title}</span>
            <ul className="sidebar-list">
              {d.messages.map((m,key) => (
                <SideListItem
                  key={key}
                  message={m}
                  sendAnalyticsEvent={this.props.sendAnalyticsEvent}
                />
              ))}
            </ul>
          </div>
        ))}
        </div>
      </aside>
    )
  }
}

Sidebar.propTypes = {
  content: PropTypes.object.isRequired,
  markRead: PropTypes.func.isRequired,
  markUnRead: PropTypes.func.isRequired,
  additionalClasses: PropTypes.string,
  sendAnalyticsEvent: PropTypes.func.isRequired
}

export default Sidebar
