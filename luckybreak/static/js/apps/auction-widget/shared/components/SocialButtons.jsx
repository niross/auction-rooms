import React from 'react';
import PropTypes from 'prop-types';
import TwitterIcon from 'mdi-react/TwitterIcon';
import FacebookBoxIcon from 'mdi-react/FacebookBoxIcon';
import EmailIcon from 'mdi-react/EmailIcon';
import { Row, Col } from 'react-materialize';

import { twitterUsername, siteName } from '../../../Config';

const propTypes = {
  shareUrl: PropTypes.string.isRequired
};
const defaultProps = {};

const SocialButtons = (props) =>
  <Row className="social-buttons">
    <Col s={4} className="center-align">
      <a href={`https://twitter.com/intent/tweet?via=${twitterUsername}&text=Check%20out%20this%20auction%20on%20${siteName}&url=${props.shareUrl}`}>
        <TwitterIcon />
      </a>
    </Col>
    <Col s={4} className="center-align">
      <a
        href="#"
        onClick={(e) => {
          e.preventDefault();
          FB.ui({
            method: 'share',
            href: props.shareUrl
          });
        }}
      >
        <FacebookBoxIcon />
      </a>
    </Col>
    <Col s={4} className="center-align">
      <a
        href={
          `mailto:?subject=Check%20out%20this%20auction%20on%20${siteName}&body=${props.shareUrl}`
        }
      >
        <EmailIcon />
      </a>
    </Col>
  </Row>;

SocialButtons.propTypes = propTypes;
SocialButtons.defaultProps = defaultProps;

export default SocialButtons;
