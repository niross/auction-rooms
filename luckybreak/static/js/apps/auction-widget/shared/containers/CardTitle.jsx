import React from 'react';
import PropTypes from 'prop-types';
import { Icon } from 'react-materialize';
import moment from 'moment';
import countdown from 'countdown';

const propTypes = {
  currentPrice: PropTypes.string.isRequired,
  bidCount: PropTypes.number.isRequired,
  endDate: PropTypes.instanceOf(moment).isRequired
};
const defaultProps = {};

const CardTitle = class extends React.Component {
  constructor(props) {
    super(props);
    countdown.setLabels(null, null, ', ', null, null);
    this.state = {
      timer: countdown(
        props.endDate,
        (ts) => {
          if (this.timer) {
            this.timer.innerHTML = ts.toString();
          }
        },
        countdown.ALL,
        2
      )
    };
  }

  /**
   * Kill the timer on unmount
   */
  componentWillUnmount() {
    window.clearInterval(this.state.timer);
  }

  /**
   * Returns true if the end date is in the next 24 hours
   */
  isEnding() {
    return this.props.endDate.isBefore(moment().add(1, 'days'));
  }

  render() {
    return (
      <div className="grey darken-3 white-text">
        <div>
          <h4 className="valign-wrapper">
            {this.props.currentPrice}&nbsp;
            <small className="grey-text text-lighten-1">
              {this.props.bidCount} bid{this.props.bidCount !== 1 ? 's' : ''}
            </small>
          </h4>
          <div>
            <h5 className="valign-wrapper">
              <Icon
                className={this.isEnding() ? 'red-text text-lighten-1' : null}
                left
              >
                access_time
              </Icon>
              {this.props.endDate.isSameOrBefore(moment()) ?
                <span>
                  Finished {this.props.endDate.format('ddd, D MMM YYYY')}
                </span>
                :
                <span
                  className={this.isEnding() ? 'red-text text-lighten-1' : null}
                >
                  <span ref={s => this.timer = s} /> remaining
                </span>
              }
            </h5>
          </div>
        </div>
      </div>
    );
  }
};

CardTitle.propTypes = propTypes;
CardTitle.defaultProps = defaultProps;

export default CardTitle;
