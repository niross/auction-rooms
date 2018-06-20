import React from 'react';
import PropTypes from 'prop-types';
import { CollectionItem, Row, Col } from 'react-materialize';
import moment from 'moment';

const propTypes = {
  avatar: PropTypes.oneOfType([PropTypes.string, PropTypes.node]).isRequired,
  title: PropTypes.string.isRequired,
  price: PropTypes.string.isRequired,
  date: PropTypes.instanceOf(moment).isRequired
};
const defaultProps = {};

const Bid = props => (
  <CollectionItem className="avatar">
    <div className="circle grey lighten-1">
      {props.avatar}
    </div>
    <Row className="header-row">
      <Col s={7} className="truncate">
        <span className="title pull">{props.title}</span>
      </Col>
      <Col s={5} className="right-align">
        <span className="push">{props.price}</span>
      </Col>
    </Row>
    <Row>
      <Col s={12}>
        <p>{props.date.format('HH:mm ddd, D MMM YYYY')}</p>
      </Col>
    </Row>
  </CollectionItem>
);


Bid.propTypes = propTypes;
Bid.defaultProps = defaultProps;

export default Bid;
