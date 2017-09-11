import React, { PropTypes } from 'react';
import { Row, Col } from 'react-bootstrap';

const propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.node.isRequired
};
const defaultProps = {};

const WizardStepHeader = (props) =>
  <span className="wizard-header">
    <Row>
      <h4 className="text-center">
        {props.title}
      </h4>
      <Col md={12} className="info text-center text-info">
        {props.children}
      </Col>
    </Row>
    <hr />
  </span>;

WizardStepHeader.propTypes = propTypes;
WizardStepHeader.defaultProps = defaultProps;

export default WizardStepHeader;
