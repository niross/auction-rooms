import React, { PropTypes } from 'react';

const propTypes = {
  text: PropTypes.string,
  size: PropTypes.oneOf([1, 2, 3, 3, 4, 5])
};
const defaultProps = {
  size: 1,
  text: ''
};

export const Spinner = ({ size, text }) =>
  <span>
    <i className={`fa fa-refresh fa-spin fa-${size}x fa-fw`} /><br />{text}
  </span>;

Spinner.propTypes = propTypes;
Spinner.defaultProps = defaultProps;
