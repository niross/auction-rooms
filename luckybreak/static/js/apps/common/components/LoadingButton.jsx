import React, { PropTypes } from 'react';
import { Button } from 'react-bootstrap';

const propTypes = {
  text: PropTypes.string.isRequired,
  style: PropTypes.oneOf(['success', 'warning', 'danger', 'default']),
  size: PropTypes.oneOf(['sm', 'lg'])
};
const defaultProps = {
  style: 'default',
  size: null
};

const LoadingButton = ({ text, style, size }) =>
  <Button bsStyle={style} bsSize={size} disabled>
    <i className="fa fa-refresh fa-spin fa-fw" /> {text}
  </Button>;

LoadingButton.propTypes = propTypes;
LoadingButton.defaultProps = defaultProps;

export default LoadingButton;
