import React from 'react';
import ReactDOM from 'react-dom';
import $ from 'jquery';

import './main.less';
import Gallery from './containers/Gallery';

$('.gallery-app').each((i, target) => {
  const images = [];
  $(target).find('.img-src').each((j, img) =>
    images.push(img.dataset));
  ReactDOM.render(
    <Gallery images={images} />,
    target
  );
});
