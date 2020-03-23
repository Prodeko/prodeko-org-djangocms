import React from 'react'
import PropTypes from 'prop-types'
import Moment from 'moment'
import Article from './Article'
import Header from './Header'
import TableOfContents from './TableOfContents'
import Footer from './Footer'

const Content = (props) => {
  const { additionalClasses, sendAnalyticsEvent, content } = props

  return (
    <div id="main-content" className={additionalClasses}>
      <Header />
      <TableOfContents
        content={content}
        sendAnalyticsEvent={sendAnalyticsEvent}
      />
      <div>
        <div>
          {content.data
            .filter((c) => c.messages.length > 0)
            .map((c, ckey) => (
              <div key={ckey}>
                <h2>{c.title}</h2>
                {c.messages.map((m, mkey) => (
                  <Article
                    key={mkey}
                    pubDate={Moment(m.pub_date).format('DD.MM.')}
                    dlDate={
                      m.show_deadline
                        ? Moment(m.deadline_date).format('DD.MM.')
                        : null
                    }
                    id={m.id}
                    title={m.header}
                    text={m.content}
                  />
                ))}
              </div>
            ))}
        </div>
      </div>
      <Footer />
    </div>
  )
}

Content.propTypes = {
  additionalClasses: PropTypes.string,
  content: PropTypes.object.isRequired,
  sendAnalyticsEvent: PropTypes.func.isRequired,
}

export default Content
