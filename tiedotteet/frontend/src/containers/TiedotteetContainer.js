import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import * as contentActions from '../redux/actions/content'
import * as analyticsActions from '../redux/actions/analytics'
import Main from '../components/Main'

const mapStateToProps = state => {
  return {
    content: state.content
  }
}

const mapDispatchToProps = dispatch => {
  return {
    contentActions: bindActionCreators(contentActions, dispatch),
    analyticsActions: bindActionCreators(analyticsActions, dispatch)
  }
}

const TiedottetContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Main)

export default TiedottetContainer
