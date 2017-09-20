import React from 'react';
import PropTypes from 'prop-types';

const propTypes = {
  children: PropTypes.node.isRequired,
  s: PropTypes.number,
  m: PropTypes.number,
  l: PropTypes.number,
  style: PropTypes.object,
  className: PropTypes.string
};
const defaultProps = {
  s: 12,
  m: 12,
  l: 12,
  style: {}
};

const styles = {
  marginBottom: '20px',
  fontSize: '12px',
  color: '#9e9e9e',
  className: ''
};

const HelpText = props => (
  <div
    className={`helptext col s${props.s} m${props.m} l${props.l} ${props.className}`}
    style={Object.assign(props.style, styles)}
  >
    {props.children}
  </div>
);

HelpText.propTypes = propTypes;
HelpText.defaultProps = defaultProps;

export default HelpText;
