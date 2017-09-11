import React, { PropTypes } from 'react';
import { Row, Col } from 'react-materialize';

const propTypes = {
  text: PropTypes.string.isRequired
};
const defaultProps = {};

const Subheader = ({ text }) => (
  <Row className="subheader">
    <Col s={12}>
      <h5>{text}</h5>
    </Col>
  </Row>
);

Subheader.propTypes = propTypes;
Subheader.defaultProps = defaultProps;

export default Subheader;
