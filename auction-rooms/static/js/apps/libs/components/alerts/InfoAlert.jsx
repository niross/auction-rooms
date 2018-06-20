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

const InfoAlert = ({ showIcon, children }) => (
  <AlertBase
    icon={showIcon ? 'info' : null}
    colour="blue lighten-1"
  >
    {children}
  </AlertBase>
);

InfoAlert.propTypes = propTypes;
InfoAlert.defaultProps = defaultProps;

export default InfoAlert;
