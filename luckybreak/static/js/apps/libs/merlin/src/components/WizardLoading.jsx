import React, { PropTypes } from 'react';

import { Preloader } from 'react-materialize';

const propTypes = {
  minHeight: PropTypes.number,
  loadingMesage: PropTypes.string
};
const defaultProps = {
  minHeight: 100,
  loadingMessage: 'Loading...'
};

const WizardLoading = ({ minHeight, loadingMessage }) =>
  <div className="wizard-loading" style={{ minHeight: `${minHeight}px` }}>
    <div>
      <Preloader flashing /> {loadingMessage}
    </div>
  </div>;

WizardLoading.propTypes = propTypes;
WizardLoading.defaultProps = defaultProps;

export default WizardLoading;
