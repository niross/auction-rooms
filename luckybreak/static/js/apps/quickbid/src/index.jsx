import React from 'react';
import ReactDOM from 'react-dom';

import './main.less';
import QuickBid from './containers/QuickBid';

$('.quickbid-app').each((i, target) => {
  ReactDOM.render(
    <QuickBid
      id={parseInt(target.dataset.id, 10)}
      title={target.dataset.title}
      currency={target.dataset.currency}
      currentBid={parseFloat(target.dataset.currentBid)}
    />,
    target
  );
});
