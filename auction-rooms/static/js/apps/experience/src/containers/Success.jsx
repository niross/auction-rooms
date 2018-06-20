import React from 'react';
import PropTypes from 'prop-types';
import { Row, Col } from 'react-materialize';

import { SuccessCheck } from '../../../libs';

const propTypes = {
  formData: PropTypes.object,
  savedExperience: PropTypes.object
};
const defaultProps = {
  formData: {},
  savedExperience: null
};

class Success extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <span className="experience-success">
        <SuccessCheck
          message={this.props.savedExperience ? 'Experience Added!' : 'Experience Updated'}
        />
        <Row>
          <Col s={12} className="center-align">
            <p>
              Your experience&nbsp;
              <strong>
                {
                  this.props.formData.savedExperience ?
                    this.props.formData.savedExperience.title
                    :
                    this.props.formData.updatedExperience.title
                }
              </strong> was&nbsp;
              {this.props.savedExperience ? 'created' : 'updated'} successfully.
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

