import React, { PropTypes } from 'react';

import AlertBase from './AlertBase';

const propTypes = {
  showIcon: PropTypes.bool,
  children: PropTypes.node.isRequired
};
const defaultProps = {
  showIcon: true
};

const SuccessAlert = ({ showIcon, children }) => (
  <AlertBase
    icon={showIcon ? 'check_circle' : null}
    colour="green lighten-1"
  >
    {children}
  </AlertBase>
);

SuccessAlert.propTypes = propTypes;
SuccessAlert.defaultProps = defaultProps;

export default SuccessAlert;
