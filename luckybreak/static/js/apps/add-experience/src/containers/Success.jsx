import React from 'react';                                                                              
import PropTypes from 'prop-types';
import { Row, Col } from 'react-materialize';

import { SuccessCheck } from '../../../libs';

const propTypes = {
  formData: PropTypes.object
};
const defaultProps = {
  formData: {}
};

class Success extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <span className="experience-success">
        <SuccessCheck message="Experience Added!" />
        <Row>
          <Col s={12} className="center-align">
            <p>
              Your experience <strong>{this.props.formData.savedExperience.title}</strong> was
              created successfully.
            </p>
            <p>
              To create an auction for this experience click the
              <strong> Create Auction</strong> button below.
            </p>
            <p>To go back to your dashboard click the <strong>Close</strong> button.</p>
          </Col>
        </Row>
      </span>
    );
  }
}

Success.propTypes = propTypes;
Success.defaultProps = defaultProps;

export default Success;

