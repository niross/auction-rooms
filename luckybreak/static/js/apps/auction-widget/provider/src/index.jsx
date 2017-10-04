import React from 'react';
import ReactDOM from 'react-dom';

import AuctionWidget from './containers/AuctionWidget';
import '../../main.less';
import './main.less';

const target = document.getElementById('provider-auction-widget-app');

ReactDOM.render(
  <AuctionWidget
    auctionId={parseInt(target.dataset.auctionId, 10)}
    currentPrice={target.dataset.currentPrice}
    bidCount={parseInt(target.dataset.bidCount, 10)}
    endDate={target.dataset.endDate}
  />,
  target
);
