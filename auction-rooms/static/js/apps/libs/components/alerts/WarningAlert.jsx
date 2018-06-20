import React from 'react';
import PropTypes from 'prop-types';

import AlertBase from './AlertBase';

const propTypes = {
  showIcon: PropTypes.bool,
  children: PropTypes.node.isRequired
};
const defaultProps = {
  showIcon: true
};

const WarningAlert = ({ showIcon, children }) => (
  <AlertBase
    icon={showIcon ? 'warning' : null}
    colour="deep-orange lighten-1"
  >
    {children}
  </AlertBase>
);

WarningAlert.propTypes = propTypes;
WarningAlert.defaultProps = defaultProps;

export default WarningAlert;
