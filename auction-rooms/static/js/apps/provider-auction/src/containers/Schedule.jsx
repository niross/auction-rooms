import React from 'react';
import PropTypes from 'prop-types';
import { Row, Col, Input } from 'react-materialize';
import moment from 'moment';

import { HelpText, Subheader } from '../../../libs';

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
      errors: {}
    };
    this.requiredFields = [
      'check_in_date', 'check_in_time', 'check_out_date', 'check_out_time'
    ];
  }

  componentDidMount() {
    $('.timepicker').pickatime({
      twelvehour: false,
      default: '11:00'
    });
    $('.checkin-time').on(
      'change', e => this.props.onFieldChange('check_in_time', e.target.value)
    );
    $('.checkout-time').on(
      'change', e => this.props.onFieldChange('check_out_time', e.target.value)
    );
  }

  getCheckIn() {
    const form = this.props.formData;
    return moment(form.check_in_date).set({
      hour: form.check_in_time.split(':')[0],
      minute: form.check_in_time.split(':')[1]
    });
  }

  getCheckOut() {
    const form = this.props.formData;
    return moment(form.check_out_date).set({
      hour: form.check_out_time.split(':')[0],
      minute: form.check_out_time.split(':')[1]
    });
  }

  handleSubmit(successCallback) {
    this.props.onFieldChange('check_in', this.getCheckIn());
    this.props.onFieldChange('check_out', this.getCheckOut());
    successCallback();
  }

  handleValidate() {
    const errors = {};

    if (this.getCheckIn() < moment()) {
      errors.check_in_date = 'Start date must be in the future';
    }

    if (this.getCheckOut() <= this.getCheckIn()) {
      errors.check_out_date = 'Check out must be after check in';
    }

    this.setState({ errors });
    return Object.keys(errors).length === 0;
  }

  render() {
    const formData = this.props.formData;
    return (
      <span>
        <Subheader text="Scheduling" />
        <Row>
          <Col s={12} m={6}>
            <Input
              s={12}
              className="with-help"
              placeholder="1 February 2029"
              label="Check In Date"
              value={
                formData.check_in_date ? formData.check_in_date.format('ddd, D MMM YYYY') : ''
              }
              labelClassName="active"
              error={this.state.errors.check_in_date}
              id="auction-checkin-date"
              name="auction-checkin-date"
              type="date"
              options={{
                closeOnSelect: true,
                format: 'ddd, D MMM YYYY',
                onStart: function () { // eslint-disable-line
                  if (formData.check_in_date) {
                    this.set('select', formData.check_in_date.toDate());
                  }
                },
                onSet: (e) => {
                  const d = moment(e.select, 'x');
                  if (d.isValid()) {
                    this.props.onFieldChange('check_in_date', d);
                    if (!formData.check_out_date || formData.check_out_date.isBefore(d)) {
                      this.props.onFieldChange('check_out_date', moment(d).add(1, 'days'));
                    }
                  }
                }
              }}
            />
            <HelpText s={12}>Enter the check in date for the experience</HelpText>
          </Col>
          <Col s={12} m={6}>
            <Input
              s={12}
              className="with-help timepicker checkin-time"
              placeholder="14:00"
              label="Check In Time"
              value={this.props.formData.check_in_time}
              labelClassName="active"
              error={this.state.errors.check_in_time}
              id="auction-checkin-time"
              name="auction-checkin-time"
            />
            <HelpText s={12}>Enter the time guests can check in</HelpText>
          </Col>
        </Row>
        <Row>
          <Col s={12} m={6}>
            <Input
              s={12}
              className="with-help"
              placeholder="2 February 2029"
              label="Check Out Date"
              value={
                formData.check_out_date ? formData.check_out_date.format('ddd, D MMM YYYY') : ''
              }
              labelClassName="active"
              error={this.state.errors.check_out_date}
              id="auction-checkout-date"
              name="auction-checkout-date"
              type="date"
              options={{
                closeOnSelect: true,
                format: 'ddd, D MMM YYYY',
                onStart: function () { // eslint-disable-line
                  if (formData.check_out_date) {
                    this.set('select', formData.check_out_date.toDate());
                  }
                },
                onSet: e => this.props.onFieldChange('check_out_date', moment(e.select, 'x'))
              }}
            />
            <HelpText s={12}>Enter the check out date for the experience</HelpText>
          </Col>
          <Col s={12} m={6}>
            <Input
              s={12}
              className="with-help timepicker checkout-time"
              placeholder="11:00"
              label="Check Out Time"
              value={this.props.formData.check_out_time}
              labelClassName="active"
              error={this.state.errors.check_out_time}
              id="auction-checkout-time"
              name="auction-checkout-time"
            />
            <HelpText s={12}>Enter the time guests can check out</HelpText>
          </Col>
        </Row>
      </span>
    );
  }
}

Schedule.propTypes = propTypes;
Schedule.defaultProps = defaultProps;

export default Schedule;

