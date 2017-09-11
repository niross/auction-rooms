import React, { PropTypes } from 'react';

import { AuthCompleteForm } from '../../../authenticator';

const propTypes = {
  isAuthenticated: PropTypes.bool,
  onSkip: PropTypes.func
};
const defaultProps = {
  isAuthenticated: false,
  onSkip: () => {}
};

class WizardAuthCompleteForm extends React.Component {
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
      <AuthCompleteForm
        ref={form => this.form = form}
        {...this.props}
      />
    );
  }
}

WizardAuthCompleteForm.propTypes = propTypes;
WizardAuthCompleteForm.defaultProps = defaultProps;

export default WizardAuthCompleteForm;
