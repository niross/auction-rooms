import React from 'react';
import ReactDOM from 'react-dom';

import './main.less';
import AddExperience from './containers/AddExperience';

$('.add-experience-app').each((i, target) => {
  ReactDOM.render(
    <AddExperience />,
    target
  );
});
