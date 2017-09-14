import React from 'react';
import PropTypes from 'prop-types';
import { Row, Col, Icon } from 'react-materialize';

const propTypes = {
  message: PropTypes.string.isRequired
};
const defaultProps = {};

const SuccessCheck = props => (
  <Row className="success-check center-align">
    <Col s={12}>
      <Icon large className="green-text">check_circle</Icon>
      <h4>{props.message}</h4>
    </Col>
  </Row>
);

SuccessCheck.propTypes = propTypes;
SuccessCheck.defaultProps = defaultProps;

export default SuccessCheck;
