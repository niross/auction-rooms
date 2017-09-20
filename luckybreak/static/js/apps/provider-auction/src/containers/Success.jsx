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
    const auctions = this.props.formData.auctions;
    const numAuctions = auctions.length;
    return (
      <span className="auction-success">
        <SuccessCheck message={`Auction${numAuctions > 1 ? 's' : ''} Added!`} />
        <Row>
          <Col s={12} className="center-align">
            <p>
              Your {numAuctions === 1 ? 'auction' : `${numAuctions} auctions`} of&nbsp;
              <strong>{auctions[0].experience.title}</strong>&nbsp;
              {numAuctions === 1 ? 'was' : 'were'} created successfully.
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
