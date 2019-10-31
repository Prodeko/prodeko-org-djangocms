import React, { useState, useEffect, useCallback } from 'react'
import PropTypes from 'prop-types'
import Loader from './Loader'
import Sidebar from './Sidebar'
import MainContent from './Content'
import MenuControl from './MenuControl'
import ScrollControl from './ScrollControl'
import Hammer from 'react-hammerjs'

const sidebarDimensions = {
  width: 260,
  handle: 0,
  desktopLimit: 660,
  initiallyOpen: true
}

const Content = props => {
  const { analyticsActions, contentActions, content } = props
  const { markRead, markUnread, fetchContent } = contentActions
  const { sendAnalyticsEvent } = analyticsActions

  const [showScrollButton, setShowScrollbutton] = useState(
    window.pageYOffset > 300
  )
  const [mode, setMode] = useState(null)
  const [sidebarOpen, setSidebarOpen] = useState(
    sidebarDimensions.initiallyOpen
  )

  const updateDimensions = useCallback(() => {
    const desktopWidth = window.innerWidth > sidebarDimensions.desktopLimit
    const m = desktopWidth ? 'desktop' : 'mobile'
    if (m !== mode) {
      setMode(m)
      setSidebarOpen(m === 'desktop')
    }
  }, [mode])

  const handleScroll = useCallback(() => {
    if (window.pageYOffset > 300 && !showScrollButton) {
      setShowScrollbutton(true)
    }
    if (window.pageYOffset <= 300 && showScrollButton) {
      setShowScrollbutton(false)
    }
  }, [mode, showScrollButton])

  useEffect(() => {
    fetchContent()
  }, [])

  useEffect(() => {
    window.addEventListener('resize', updateDimensions)
    window.addEventListener('scroll', handleScroll)

    updateDimensions()

    return () => {
      window.removeEventListener('resize', updateDimensions)
      window.removeEventListener('resize', handleScroll)
    }
  }, [updateDimensions, handleScroll])

  const toggleSidebar = () => {
    setSidebarOpen(open => !open)
  }

  const handleSwipe = e => {
    if (mode === 'mobile') {
      const d = e.direction
      if ((sidebarOpen && d == 2) || (!sidebarOpen && d == 4)) {
        toggleSidebar()
      }
    }
  }

  return content.isFetching ? (
    <Loader />
  ) : (
    <Hammer onSwipe={handleSwipe}>
      <div id="wrapper">
        <Sidebar
          additionalClasses={`${sidebarOpen ? 'open' : 'closed'}`}
          content={content}
          markRead={markRead}
          markUnread={markUnread}
          sendAnalyticsEvent={sendAnalyticsEvent}
        />
        <MainContent
          additionalClasses={`${
            sidebarOpen ? 'sidebar-open' : 'sidebar-closed'
          } ${mode === 'mobile' ? 'display-mobile' : 'display-desktop'}`}
          content={content}
          sendAnalyticsEvent={sendAnalyticsEvent}
        />
        {mode === 'mobile' && (
          <MenuControl handleClick={() => toggleSidebar()} />
        )}
        {showScrollButton && (
          <ScrollControl handleClick={() => window.scroll(0, 0)} />
        )}
      </div>
    </Hammer>
  )
}

Content.propTypes = {
  content: PropTypes.object.isRequired
}

export default Content
