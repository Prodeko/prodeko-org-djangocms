import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Loader from '../../components/Loader'
import Sidebar from './Sidebar'
import MainContent from './MainContent'
import MenuControl from '../../components/MenuControl'
import ScrollControl from '../../components/ScrollControl'
import Hammer from 'react-hammerjs'

const sidebarDimensions = {
  width: 260,
  handle: 0,
  desktopLimit: 660,
  initiallyOpen: true
}

class Content extends Component {

  constructor(props) {
    super(props)
    this.state = {
      showScrollButton: window.pageYOffset > 300,
      displayMode: null,
      sidebarOpen: sidebarDimensions.initiallyOpen
    }
  }

  componentWillMount() {
    this.props.Contentactions.fetchContent()
  }

  componentDidMount() {
    window.addEventListener("resize", this.updateDimensions)
    window.addEventListener("scroll", this.handleScroll)
    this.updateDimensions()
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.updateDimensions)
    window.removeEventListener("scroll", this.handleScroll)
  }

  updateDimensions = () => {
    const desktopWidth = window.innerWidth > sidebarDimensions.desktopLimit;
    const displayMode = desktopWidth ? "desktop" : "mobile"
    if (displayMode !== this.state.displayMode) {
      this.setState({
        displayMode: displayMode,
        sidebarOpen: displayMode === "desktop"
      })
    }
  }

  handleScroll = () => {
    if (window.pageYOffset > 300 && !this.state.showScrollButton) {
      this.setState({showScrollButton: true})
    }
    if (window.pageYOffset <= 300 && this.state.showScrollButton) {
      this.setState({showScrollButton: false})
    }
  }

  handleMenuButtonClick = () => {
    this.props.Analyticsactions.sendAnalyticsEvent('Menu button', 'press')
    this.toggleSidebar()
  }

  toggleSidebar = () => {
    this.setState({sidebarOpen: !this.state.sidebarOpen})
  }

  scrollUp = () => {
    this.props.Analyticsactions.sendAnalyticsEvent('Scroll-up button', 'press')
    window.scroll(0,0)
  }

  handleSwipe = (e) => {
    if (this.state.displayMode === "mobile") {
      this.props.Analyticsactions.sendAnalyticsEvent('Sidebar', 'swipe')
      const d = e.direction
      if ((this.state.sidebarOpen && d == 2) || (!this.state.sidebarOpen && d == 4)) {
        this.toggleSidebar()
      }
    }
  }

  render() {
    if (this.props.content.isFetching) {
      return <Loader/>
    }
    return (
      <Hammer onSwipe={this.handleSwipe}>
        <div id="wrapper">
          <Sidebar
            additionalClasses={`${this.state.sidebarOpen ? 'open' : 'closed'}`}
            content={this.props.content}
            markRead={this.props.Contentactions.markRead}
            markUnRead={this.props.Contentactions.markUnRead}
            sendAnalyticsEvent={this.props.Analyticsactions.sendAnalyticsEvent}
          />
          <MainContent
            additionalClasses={`${this.state.sidebarOpen ? 'sidebar-open' : 'sidebar-closed'} ${this.state.displayMode === 'mobile' ? 'display-mobile' : 'display-desktop'}`}
            content={this.props.content}
            sendAnalyticsEvent={this.props.Analyticsactions.sendAnalyticsEvent}
          />
          {this.state.displayMode === "mobile" &&
            <MenuControl handleClick={this.handleMenuButtonClick}/>
          }
          {this.state.showScrollButton &&
            <ScrollControl handleClick={this.scrollUp}/>
          }
        </div>
      </Hammer>
    )
  }
}

Content.propTypes = {
  content: PropTypes.object.isRequired,
}

export default Content
