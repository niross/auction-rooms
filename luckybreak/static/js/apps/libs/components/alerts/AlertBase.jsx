import React from 'react';
import PropTypes from 'prop-types';
import { Card } from 'react-materialize';

const propTypes = {
  icon: PropTypes.string,
  colour: PropTypes.string.isRequired,
  children: PropTypes.node.isRequired
};
const defaultProps = {
  icon: null
};

const AlertBase = props => (
  <Card className={`white-text valign-wrapper ${props.colour}`}>
    {props.icon ?
      <span>
        <i className="material-icons left">{props.icon}</i>
      </span>
      : null
    }
    {props.children}
  </Card>
);

AlertBase.propTypes = propTypes;
AlertBase.defaultProps = defaultProps;

export default AlertBase;
