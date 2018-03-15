import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Moment from 'moment'
import Article from '../../components/Article'
import Header from '../../components/Header'
import TableOfContents from '../../components/TableOfContents'
import Footer from '../../components/Footer'
import LoginForm from '../../components/LoginForm'
import LogoutForm from '../../components/LogoutForm'

class MainContent extends Component {
  render() {
    return (
      <div id="main-content" className={this.props.additionalClasses}>
        {window.user === "AnonymousUser" ?
          <LoginForm/> :
          <LogoutForm/>
        }

        <Header/>
        <TableOfContents content={this.props.content} sendAnalyticsEvent={this.props.sendAnalyticsEvent}/>
        <div>
          <div>
            {this.props.content.data.filter(c => c.messages.length > 0).map((c,ckey) => {
              return(
                <div key={ckey}>
                  <h2>{c.title}</h2>
                  {c.messages.map((m, mkey) => {
                    return(
                      <Article
                        key={mkey}
                        pubDate={Moment(m.pub_date).format("DD.MM.")}
                        dlDate={m.show_deadline ? Moment(m.deadline_date).format("DD.MM.") : null}
                        id={m.id}
                        title={m.header}
                        text={m.content}
                      />
                    )
                  })}
                </div>
              )
            })}
          </div>
        </div>
        <Footer/>
      </div>
    )
  }
}

MainContent.propTypes = {
  additionalClasses: PropTypes.string,
  content: PropTypes.object.isRequired,
  sendAnalyticsEvent: PropTypes.func.isRequired
}

export default MainContent
