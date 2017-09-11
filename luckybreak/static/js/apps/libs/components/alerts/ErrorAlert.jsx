import React, { PropTypes } from 'react';

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
    icon={showIcon ? 'error' : null}
    colour="red lighten-1"
  >
    {children}
  </AlertBase>
);

InfoAlert.propTypes = propTypes;
InfoAlert.defaultProps = defaultProps;

export default InfoAlert;
