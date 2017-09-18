import React from 'react';
import ReactDOM from 'react-dom';

import './main.less';
import Auction from './containers/Auction';

$('.provider-auction-app').each((i, target) => {
  const data = $(target).data();
  ReactDOM.render(
    <Auction
      modalId={data.modalId}
      auctionId={data.auctionId}
      experienceId={data.experienceId}
      buttonFloating={data.buttonFloating != null}
      buttonWaves={data.buttonWaves}
      buttonColour={data.buttonColour}
      buttonId={data.buttonId}
      buttonIcon={data.buttonIcon}
      buttonText={data.buttonText}
    />,
    target
  );
});
