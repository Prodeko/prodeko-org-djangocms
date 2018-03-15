import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Moment from 'moment'
import {isInStore} from '../util/localStorage'

class SideListItem extends Component {

  handleClick = () => {
    this.props.sendAnalyticsEvent('sidebar link', 'click', this.props.message.header, this.props.message.isNew ? 1 : 0)
  }

  render() {
    const m = this.props.message
    return (
      <li className={`sidebar-list-item ${isInStore(m.id) ? 'read' : ''} ${m.isNew ? 'new' : ''}`}>
        <a htmlFor={m.id} href={`#${m.id}`} onClick={this.handleClick}>
          {m.is_new &&
            <div className="icon-container text-red">
              <span>New</span>
            </div>
          }
          {m.show_deadline &&
          <div className="icon-container text-light-grey">
            <span>DL: {Moment(m.deadline_date).format("D.M.Y")}</span>
          </div>
          }
          <div className="text-container">
            {m.header}
          </div>
        </a>
      </li>
    )
  }
}

SideListItem.propTypes = {
  message: PropTypes.object.isRequired,
  sendAnalyticsEvent: PropTypes.func.isRequired
}

export default SideListItem
