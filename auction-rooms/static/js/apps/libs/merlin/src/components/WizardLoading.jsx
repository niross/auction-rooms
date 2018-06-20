import React from 'react';
import PropTypes from 'prop-types';

import { Preloader } from 'react-materialize';

const propTypes = {
  minHeight: PropTypes.number,
  loadingMessage: PropTypes.string
};
const defaultProps = {
  minHeight: 100,
  loadingMessage: null
};

const WizardLoading = ({ minHeight, loadingMessage }) => (
  <div className="wizard-loading valign-wrapper center-align" style={{ minHeight: '400px' }}>
    <div style={{ width: '100%' }}>
      <Preloader flashing />
      {loadingMessage ? <span><br />loadingMessage</span> : null}
    </div>
  </div>
);

WizardLoading.propTypes = propTypes;
WizardLoading.defaultProps = defaultProps;

export default WizardLoading;
