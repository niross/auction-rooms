import React from 'react';
import ReactDOM from 'react-dom';

import GuestAuctionWidget from './containers/GuestAuctionWidget';
import '../../main.less';
import './main.less';

const target = document.getElementById('guest-auction-widget-app');

ReactDOM.render(
  <GuestAuctionWidget
    auctionId={parseInt(target.dataset.auctionId, 10)}
    currentPrice={target.dataset.currentPrice}
    actualPrice={parseFloat(target.dataset.actualPrice)}
    bidCount={parseInt(target.dataset.bidCount, 10)}
    endDate={target.dataset.endDate}
    authenticated={target.dataset.authenticated != null}
    favourited={target.dataset.favourited != null}
    title={target.dataset.title}
    currencySymbol={target.dataset.currencySymbol}
    userId={target.dataset.userId ? parseInt(target.dataset.userId, 10) : null}
    highestBidderId={
      target.dataset.highestBidderId ? parseInt(target.dataset.highestBidderId, 10) : null
    }
    debug={target.dataset.debug != null}
  />,
  target
);
