import React from 'react';
import { Card, Row, Col, Icon, Button, Input } from 'react-materialize';
import moment from 'moment';

import CardTitle from '../../../shared/containers/CardTitle';
import SocketErrorMask from '../../../shared/components/SocketErrorMask';
import BaseWidget from '../../../shared/containers/BaseWidget';
import SocialButtons from '../../../shared/components/SocialButtons';
import { apiEndpoints } from '../../../../Config';
import { makeApiCall, successToast, warningToast, InfoAlert } from '../../../../libs';
import ConfirmModal from '../components/ConfirmModal';

const GuestAuctionWidget = class extends BaseWidget {
  componentWillMount() {
    this.setState({
      loading: false,
      nextBid: (parseFloat(this.state.actualPrice) + 1).toFixed(2),
      bidding: false,
      favouriting: false
    });
  }

  handleData(jsonData) {
    const data = JSON.parse(jsonData);
    if (this.state.highestBidderId === this.props.userId &&
        data.highest_bidder !== this.props.userId) {
      warningToast('Oops, You have been out bid!');
    }
    this.setState({
      bidError: null,
      bidCount: data.bids,
      currentPrice: data.formatted_current_price,
      actualPrice: data.current_price,
      highestBidderId: data.highest_bidder,
      nextBid: data.current_price >= parseFloat(this.state.nextBid) ?
        data.current_price + 1 : parseFloat(this.state.nextBid).toFixed(2)
    });
  }

  getSocketUrl() {
    const protocol = this.props.debug ? 'ws' : 'wss';
    const host = window.location.host;
    return `${protocol}://${host}/ws/public/auctions/${this.props.auctionId}/stream/`;
  }

  validateBid() {
    if (parseFloat(this.state.nextBid) < this.state.currentPrice + 1) {
      this.setState({
        bidError: `Minimum bid is ${(this.state.actualPrice + 1).toFixed(2)}`
      });
      return false;
    }
    return true;
  }

  placeBid() {
    if (this.validateBid()) {
      this.setState({ bidding: true, bidError: null });
      makeApiCall(
        apiEndpoints.auctionBid.replace('<id>', this.props.auctionId),
        'POST',
        { price: this.state.nextBid }
      )
        .then(() => {
          this.setState({
            bidding: false,
            nextBid: parseFloat(this.state.nextBid) + 1
          });
          successToast('Your bid was placed successfully!');
        })
        .catch(err =>
          this.setState({
            bidding: false,
            bidError: err.fieldErrors.price
          })
        );
    }
  }

  toggleFavourite() {
    this.setState({ favouriting: true });
    if (this.state.favourited) {
      makeApiCall(
        `${apiEndpoints.favourites}${this.props.auctionId}/`,
        'DELETE',
        null,
        false
      )
        .then(() =>
          this.setState({ favourited: false, favouriting: false })
        );
    }
    else {
      makeApiCall(apiEndpoints.favourites, 'POST', {
        auction: this.props.auctionId
      })
        .then(() =>
          this.setState({ favourited: true, favouriting: false })
        );
    }
  }

  render() {
    return (
      <Card
        className="auction-widget"
        title={
          <CardTitle
            {...this.state}
          />
        }
      >
        {this.state.isLive && this.props.userId === this.state.highestBidderId ?
          <InfoAlert size="s12">
            <p>Congrats! You are the highest bidder!</p>
          </InfoAlert>
          : null
        }

        {this.state.isLive && !this.state.socketOpen ?
          <SocketErrorMask />
          : null}
        {this.state.endDate.isAfter(moment()) ?
          <div className="card-body">
            <Row>
              <Col s={12} className="next-bid">
                <Input
                  s={12}
                  label="Enter your next bid"
                  validate
                  value={this.state.nextBid}
                  onChange={e => {
                    if (!isNaN(parseFloat(e.target.value)) && isFinite(e.target.value)) {
                      this.setState({ nextBid: e.target.value });
                    }
                  }}
                  error={this.state.bidError}
                >
                  <span>£</span>
                </Input>
                {this.props.authenticated ?
                  <ConfirmModal
                    bid={parseFloat(this.state.nextBid)}
                    disabled={
                      this.state.bidding || this.state.highestBidderId === this.props.userId
                    }
                    placeBid={() => this.placeBid()}
                    title={this.props.title}
                    currencySymbol={this.props.currencySymbol}
                  />
                  :
                  <a
                    href={`/accounts/login/?next=${window.location.pathname}`}
                    className="btn green white-text btn-large bid"
                  >
                    <Icon left>check_circle</Icon>Place Bid
                  </a>
                }
              </Col>
            </Row>
            <Row>
              <Col s={12}>
                <div className="divider" />
              </Col>
            </Row>
            <Row>
              <Col s={12}>
                <Button
                  waves="light"
                  large
                  className="favourite grey lighten-2 grey-text text-darken-3"
                  disabled={this.state.favouriting}
                  onClick={() => {
                    // If the user is not authenticated redirect them
                    if (!this.props.authenticated) {
                      this.redirectToLogin(true);
                    }
                    // Otherwise save the favourite
                    else {
                      this.toggleFavourite();
                    }
                  }}
                >
                  {this.state.favourited ?
                    <span>
                      <Icon left>favorite</Icon>Unfavourite
                    </span>
                    :
                    <span>
                      <Icon left>favorite_border</Icon>Favourite
                    </span>
                  }
                </Button>
              </Col>
            </Row>
            <SocialButtons shareUrl={window.location.href} />
          </div>
          : null}
      </Card>
    );
  }
};

export default GuestAuctionWidget;
