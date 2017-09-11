import React, { PropTypes } from 'react';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';

const propTypes = {};
const defaultProps = {};

const FormInputRequired = () =>
  <OverlayTrigger
    placement="top"
    overlay={<Tooltip id="req">This field is required</Tooltip>}
  >
    <i className="fa fa-asterisk required-icon" />
  </OverlayTrigger>;

FormInputRequired.propTypes = propTypes;
FormInputRequired.defaultProps = defaultProps;

export default FormInputRequired;
