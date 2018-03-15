import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'
import * as ContentActions from './ContentState'
import * as AnalyticsActions from '../Analytics/AnalyticsState'
import ContentView from './ContentView'

export default connect(
  state => ({
    content: state.content,
  }),
  dispatch => {
    return {
      Contentactions: bindActionCreators(ContentActions, dispatch),
      Analyticsactions: bindActionCreators(AnalyticsActions, dispatch)
    }
  }
)(ContentView)
