import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import WebSocket from 'reconnectingwebsocket';

const propTypes = {
  currentPrice: PropTypes.string.isRequired,
  bidCount: PropTypes.number.isRequired,
  endDate: PropTypes.string.isRequired,
  actualPrice: PropTypes.number.isRequired,
  favourited: PropTypes.bool,
  highestBidderId: PropTypes.number,
  debug: PropTypes.bool // eslint-disable-line react/no-unused-prop-types
};
const defaultProps = {
  authenticated: false,
  favourited: false,
  highestBidderId: null,
  debug: false
};

const AuctionWidget = class extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      currentPrice: props.currentPrice,
      actualPrice: props.actualPrice,
      bidCount: props.bidCount,
      bids: [],
      endDate: moment(props.endDate),
      isLive: moment(props.endDate).isAfter(moment()),
      favourited: this.props.favourited,
      highestBidderId: this.props.highestBidderId
    };

    if (this.state.isLive) {
      this.initSocket();
    }
  }

  componentWillUnmount() {
    if (this.socket) this.socket.close();
  }

  initSocket() {
    this.socket = new WebSocket(this.getSocketUrl());
    this.socket.onmessage = message => this.handleData(message.data);
    this.socket.onopen = () => this.setState({ socketOpen: true });
    this.socket.onclose = () => this.setState({ socketOpen: false });
  }
};

AuctionWidget.propTypes = propTypes;
AuctionWidget.defaultProps = defaultProps;

export default AuctionWidget;
