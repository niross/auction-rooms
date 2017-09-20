import React from 'react';
import PropTypes from 'prop-types';
import { Row, Col, Input } from 'react-materialize';
import moment from 'moment';

import { HelpText, makeApiCall, WarningAlert, Subheader } from '../../../libs';
import { apiEndpoints } from '../../../Config';

const propTypes = {
  formData: PropTypes.object,
  onFieldChange: PropTypes.func
};
const defaultProps = {
  formData: {},
  onFieldChange: () => {}
};

class Schedule extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      errors: {},
      submissionErrors: {}
    };
    this.requiredFields = ['starting_price', 'reserve_price', 'duration_days', 'lots'];
  }

  handleValidate() {
    // Ensure the auction end date is before the check in date
    const endDate = moment().add(this.props.formData.duration_days, 'days');
    if (endDate.isSameOrAfter(this.props.formData.check_in)) {
      this.setState({
        submissionErrors: {
          'Auction Duration': 'Please ensure auction ends before the check in date/time'
        }
      });
      return false;
    }
    return true;
  }

  handleSubmit(successCallback, errorCallback) {
    errorCallback();
    makeApiCall(apiEndpoints.providerAuctions, 'POST', this.props.formData, true)
      .then((resp) => {
        this.props.onFieldChange('auctions', resp);
        successCallback();
      })
      .catch((err) => {
        this.setState({ submissionErrors: err.fieldErrors });
        errorCallback();
      });
  }

  render() {
    const formData = this.props.formData;
    console.log('Submissoin errors', this.state.submissionErrors);
    return (
      <span>
        {Object.keys(this.state.submissionErrors).length > 0 ?
          <WarningAlert>
            Oops, That didn&#39;t go as planned. Please fix the errors below.
            <ul>
              {Object.keys(this.state.submissionErrors).map(e =>
                <li><strong>{e}:</strong> {this.state.submissionErrors[e]}</li>
              )}
            </ul>
          </WarningAlert>
          : null}
        <Subheader text="Pricing" />
        <Row>
          <Col s={12} m={6}>
            <Input
              s={12}
              className="with-help"
              placeholder="99.99"
              label="Starting Price"
              value={formData.starting_price}
              labelClassName="active"
              error={this.state.errors.starting_price}
              id="experience-starting-price"
              name="experience-starting-price"
              type="number"
              onChange={e => this.props.onFieldChange('starting_price', e.target.value)}
              step="0.1"
              min="0"
            >
              <span>£</span>
            </Input>
            <HelpText s={12} className="right-align">
              The price that the auction will start at
            </HelpText>
          </Col>
          <Col s={12} m={6}>
            <Input
              s={12}
              className="with-help"
              placeholder="199.99"
              label="Reserve Price"
              value={formData.reserve_price}
              labelClassName="active"
              error={this.state.errors.reserve_price}
              id="experience-reserve-price"
              name="experience-reserve-price"
              type="number"
              onChange={e => this.props.onFieldChange('reserve_price', e.target.value)}
              step="0.1"
              min="0"
            >
              <span>£</span>
            </Input>
            <HelpText s={12} className="right-align">
              The minimum price you will accept
            </HelpText>
          </Col>
        </Row>
        <Subheader text="Auction Settings" />
        <Row>
          <Col s={12} m={6}>
            <Input
              s={12}
              className="with-help"
              label="Auction Duration"
              value={formData.duration_days}
              labelClassName="active"
              error={this.state.errors.duration_days}
              id="experience-duration"
              name="experience-duration"
              type="select"
              onChange={e => this.props.onFieldChange('duration_days', e.target.value)}
            >
              <option value="1">1 Day</option>
              <option value="3">3 Days</option>
              <option value="5">5 Days</option>
              <option value="7">7 Days</option>
            </Input>
            <HelpText s={12}>How long the auction will be live for</HelpText>
          </Col>
          <Col s={12} m={6}>
            <Input
              s={12}
              className="with-help"
              label="Number of Lots"
              value={formData.lots}
              labelClassName="active"
              error={this.state.errors.lots}
              id="experience-lots"
              name="experience-lots"
              type="number"
              onChange={e => this.props.onFieldChange('lots', e.target.value)}
              step="1"
              min="1"
            />
            <HelpText s={12}>
              The number of auctions to create for this experience
            </HelpText>
          </Col>
        </Row>
      </span>
    );
  }
}

Schedule.propTypes = propTypes;
Schedule.defaultProps = defaultProps;

export default Schedule;

