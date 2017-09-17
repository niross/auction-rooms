import React from 'react';
import ReactDOM from 'react-dom';

import './main.less';
import Experience from './containers/Experience';

$('.experience-app').each((i, target) => {
  const data = $(target).data();
  ReactDOM.render(
    <Experience
      modalId={data.modalId}
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
