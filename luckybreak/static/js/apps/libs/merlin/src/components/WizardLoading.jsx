import React from 'react';
import PropTypes from 'prop-types';

import { Preloader } from 'react-materialize';

const propTypes = {
  minHeight: PropTypes.number,
  loadingMessage: PropTypes.string
};
const defaultProps = {
  minHeight: 100,
  loadingMessage: 'Loading...'
};

const WizardLoading = ({ minHeight, loadingMessage }) => (
  <div className="wizard-loading" style={{ minHeight: `${minHeight}px` }}>
    <div>
      <Preloader flashing /> {loadingMessage}
    </div>
  </div>
);

WizardLoading.propTypes = propTypes;
WizardLoading.defaultProps = defaultProps;

export default WizardLoading;
