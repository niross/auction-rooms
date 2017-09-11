import React, { PropTypes } from 'react';
import { Row, Col } from 'react-bootstrap';

import { AuthEmailForm } from '../../../authenticator';

const propTypes = {
  isAuthenticated: PropTypes.bool.isRequired,
  onSkip: PropTypes.func.isRequired
};
const defaultProps = {};

class WizardAuthEmailForm extends React.Component {
  componentDidMount() {
    // If the user is already authenticated skip this step
    if (this.props.isAuthenticated) {
      this.props.onSkip();
    }
  }

  handleValidate() {
    // Call validate on the wrapped component
    return this.form.handleValidate();
  }

  handleSubmit(successCallback, errorCallback) {
    // Call submit on the wrapped component
    this.form.handleSubmit(successCallback, errorCallback);
  }

  render() {
    return (
      <AuthEmailForm
        ref={form => this.form = form}
        {...this.props}
      />
    );
  }
}

WizardAuthEmailForm.propTypes = propTypes;
WizardAuthEmailForm.defaultProps = defaultProps;

export default WizardAuthEmailForm;
