import React from 'react';
import PropTypes from 'prop-types';

import AlertBase from './AlertBase';

const propTypes = {
  showIcon: PropTypes.bool,
  children: PropTypes.node.isRequired,
  size: PropTypes.string
};
const defaultProps = {
  showIcon: true,
  size: null
};

const InfoAlert = ({ showIcon, children, size }) => (
  <AlertBase
    icon={showIcon ? 'error' : null}
    colour="red lighten-1"
    size={size}
  >
    {children}
  </AlertBase>
);

InfoAlert.propTypes = propTypes;
InfoAlert.defaultProps = defaultProps;

export default InfoAlert;
