import React, { PropTypes } from 'react';

import WizardStep from './WizardStep';

const propTypes = {};
const defaultProps = {};

class WizardAuthStep extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  handleValidate() { 
    // Call validate on the wrapper component
    return this.step.handleValidate();
  }

  handleSubmit(successCallback, errorCallback) {
    // Call submit on the wrapper component
    this.step.handleSubmit(successCallback, errorCallback);
  }

  render() {
    return (
      <WizardStep ref={(step) => this.step = step}>
        <div>hi</div>
      </WizardStep>
    );
  }
}

WizardAuthStep.propTypes = propTypes;
WizardAuthStep.defaultProps = defaultProps;

export default WizardAuthStep;

