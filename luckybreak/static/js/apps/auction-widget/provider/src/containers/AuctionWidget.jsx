import React from 'react';
import PropTypes from 'prop-types';
import { Card, Collection, ProgressBar, Icon } from 'react-materialize';
import moment from 'moment';
import WebSocket from 'reconnectingwebsocket';

import CardTitle from '../../../shared/containers/CardTitle';
import { makeApiCall } from '../../../../libs/utils/request';
import { apiEndpoints } from '../../../../Config';
import Bid from '../components/Bid';
import SocketErrorMask from '../components/SocketErrorMask';

const propTypes = {
  auctionId: PropTypes.number.isRequired,
  currentPrice: PropTypes.string.isRequired,
  bidCount: PropTypes.number.isRequired,
  endDate: PropTypes.string.isRequired
};
const defaultProps = {};

const AuctionWidget = class extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      currentPrice: props.currentPrice,
      bidCount: props.bidCount,
      bids: [],
      endDate: moment(props.endDate)
    };

    this.socket = new WebSocket(
      `ws://${window.location.host}/provider/auctions/${this.props.auctionId}/stream/`
    );
    this.socket.onmessage = message => this.handleData(message.data);
    this.socket.onopen = () => this.setState({ socketOpen: true });
    this.socket.onclose = () => this.setState({ socketOpen: false });
  }

  componentDidMount() {
    makeApiCall(`${apiEndpoints.providerAuctions}${this.props.auctionId}/`, 'GET')
      .then((resp) => {
        const bids = [...new Set(this.state.bids.concat(resp.bids))];
        this.setState({
          currentPrice: resp.formatted_current_price,
          bidCount: bids.length,
          bids,
          loading: false,
          auction: resp
        });
      });
  }

  componentWillUnmount() {
    this.socket.close();
  }

  handleData(data) {
    let bids = this.state.bids;
    bids.splice(0, 0, JSON.parse(data));
    bids = bids.sort((a, b) => b.price - a.price);
    this.setState({
      bidCount: bids.length,
      bids,
      currentPrice: bids[0].formatted_price
    });
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
        {!this.state.socketOpen ?
          <SocketErrorMask /> : null}
        <div className="card-body">
          {this.state.loading ?
            <ProgressBar />
            :
            <div>
              <Collection>
                {this.state.bids.map(bid => (
                  <Bid
                    key={`bid-${bid.id}`}
                    title={`${bid.user.first_name} ${bid.user.last_name}`}
                    avatar={bid.user.first_name[0].toUpperCase()}
                    price={bid.formatted_price}
                    date={moment(bid.created)}
                  />
                ))}
                <Bid
                  title="Auction Started"
                  avatar={<Icon>timer</Icon>}
                  price={this.state.auction.formatted_starting_price}
                  date={moment(this.state.auction.created)}
                />
              </Collection>
            </div>
          }
        </div>
      </Card>
    );
  }
};

AuctionWidget.propTypes = propTypes;
AuctionWidget.defaultProps = defaultProps;

export default AuctionWidget;
