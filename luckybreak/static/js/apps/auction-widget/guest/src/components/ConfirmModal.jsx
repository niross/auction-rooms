import React from 'react';
import PropTypes from 'prop-types';
import { Modal, Button, Icon, Row, Col } from 'react-materialize';

const propTypes = {
  bid: PropTypes.number.isRequired,
  disabled: PropTypes.bool.isRequired,
  placeBid: PropTypes.func.isRequired,
  currencySymbol: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired
};
const defaultProps = {};

const ConfirmModal = props => (
  <Modal
    className="confirm-modal"
    header="Place Bid"
    trigger={
      <Button
        large
        waves="light"
        className="bid green white-text"
        disabled={props.disabled}
      >
        <Icon left>check_circle</Icon>Place Bid
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
          >
            <Icon left>close</Icon>No, Get me out of here
          </Button>
        </Col>
        <Col s={12} m={6}>
          <Button
            id="accept"
            large
            waves="light"
            className="green white-text modal-close"
            onClick={() => {
              props.placeBid();
            }}
          >
            <Icon left>check</Icon>Yes, Place my bid now!
          </Button>
        </Col>
      </Row>
    }
  >

    <Row>
      <Col s={12}>
        <p>
          You are about to place a bid of&nbsp;
          <strong>{props.currencySymbol}{props.bid.toFixed(2)} </strong>
          on the auction of <strong>{props.title}</strong>.
        </p>
        <p>If you are happy to proceed please click the accept button below.</p>
      </Col>
    </Row>
  </Modal>
);


ConfirmModal.propTypes = propTypes;
ConfirmModal.defaultProps = defaultProps;

export default ConfirmModal;
