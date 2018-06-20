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
    actualPrice={parseFloat(target.dataset.actualPrice)}
    bidCount={parseInt(target.dataset.bidCount, 10)}
    endDate={target.dataset.endDate}
    title={target.dataset.title}
    currencySymbol={target.dataset.currencySymbol}
    userId={target.dataset.userId ? parseInt(target.dataset.userId, 10) : null}
    debug={target.dataset.debug != null}
  />,
  target
);
