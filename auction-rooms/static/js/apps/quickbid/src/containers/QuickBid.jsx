import React from 'react';
import PropTypes from 'prop-types';
import { Input, Button, Icon, Modal, Row, Col } from 'react-materialize';
import { makeApiCall } from '../../../libs/utils/request';
import { apiEndpoints } from '../../../Config';
import { successToast } from '../../../libs/utils/toast';

const propTypes = {
  id: PropTypes.number.isRequired,
  title: PropTypes.string.isRequired,
  currency: PropTypes.string.isRequired,
  currentBid: PropTypes.number.isRequired
};
const defaultProps = {};

const QuickBid = class extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      nextBid: (props.currentBid + 1).toFixed(2)
    };
  }


  validateBid() {
    if (parseFloat(this.state.nextBid) < this.props.currentBid + 1) {
      this.setState({
        bidError: `Minimum bid is ${this.props.currency}${(this.props.currentBid + 1).toFixed(2)}`
      });
      return false;
    }
    return true;
  }

  placeBid() {
    if (this.validateBid()) {
      this.setState({ bidding: true, bidError: null });
      makeApiCall(
        apiEndpoints.auctionBid.replace('<id>', this.props.id),
        'POST',
        { price: this.state.nextBid }
      )
        .then(() => {
          successToast('Your bid was placed successfully!');
          this.setState({
            bidding: false,
            nextBid: parseFloat(this.state.nextBid) + 1
          });
          window.location.reload();
        })
        .catch(err =>
          this.setState({
            bidding: false,
            bidError: err.fieldErrors.price
          })
        );
    }
  }

  render() {
    return (
      <Modal
        id="quick-bid"
        className="confirm-modal"
        header="Place Bid"
        trigger={
          <Button
            waves="light"
            className="green"
          >
            <span>
              <Icon left>add_shopping_cart</Icon>Bid Again
            </span>
          </Button>
        }
        actions={
          <Row className="modal-actions">
            <Col s={12} m={6}>
              <Button
                id="close"
                large
                waves="light"
                className="red white-text modal-close"
                disabled={this.state.bidding}
              >
                <Icon left>close</Icon>Get me out of here
              </Button>
            </Col>
            <Col s={12} m={6}>
              <Button
                id="accept"
                large
                waves="light"
                className="green white-text"
                onClick={() => this.placeBid()}
                disabled={this.state.bidding}
              >
                <Icon left>check</Icon>Place my bid now!
              </Button>
            </Col>
          </Row>
        }
      >
        <Row>
          <Col s={12}>
            <p>
              You are about to place a bid on the auction of <strong>{this.props.title}</strong>.
            </p>
            <p>
              Please confirm the amount you would like to bid before proceeding.
            </p>
          </Col>
          <Col s={12} m={8} offset="m2">
            <Input
              s={12}
              label="Enter your next bid"
              validate
              value={this.state.nextBid}
              onChange={(e) => {
                if (!isNaN(parseFloat(e.target.value)) && isFinite(e.target.value)) {
                  this.setState({ nextBid: e.target.value });
                }
              }}
              error={this.state.bidError}
            >
              <span>£</span>
            </Input>
          </Col>
        </Row>
      </Modal>
    );
  }
};

QuickBid.propTypes = propTypes;
QuickBid.defaultProps = defaultProps;

export default QuickBid;
