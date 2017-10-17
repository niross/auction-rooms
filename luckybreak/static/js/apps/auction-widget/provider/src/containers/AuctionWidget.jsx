import React from 'react';
import { Card, Collection, ProgressBar, Icon } from 'react-materialize';
import moment from 'moment';

import CardTitle from '../../../shared/containers/CardTitle';
import Bid from '../components/Bid';
import SocketErrorMask from '../../../shared/components/SocketErrorMask';
import { makeApiCall } from '../../../../libs/utils/request';
import { apiEndpoints } from '../../../../Config';

import BaseWidget from '../../../shared/containers/BaseWidget';

const AuctionWidget = class extends BaseWidget {
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

  getSocketUrl() {
    return `ws://${window.location.host}/provider/auctions/${this.props.auctionId}/stream/`;
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
        {this.state.isLive && !this.state.socketOpen ?
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

export default AuctionWidget;
