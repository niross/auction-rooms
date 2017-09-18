import React from 'react';
import PropTypes from 'prop-types';
import { Row, Col, Input } from 'react-materialize';

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
    this.requiredFields = ['check_in', 'check_out'];
  }

  handleValidate() {
    const errors = {};
    const form = this.props.formData;

    // Validate that start is before end

    // Validate that auction will end before check in date

    if (!form.placeId && !form.latitude && !form.longitude) {
      errors.location = 'Please select a valid location';
    }
    if (form.pax_adults === 0 && form.pax_children === 0) {
      errors.pax_adults = 'An adult or child is required';
      errors.pax_children = 'An adult or child is required';
    }
    this.setState({ errors });
    return Object.keys(errors).length === 0;
  }

  // handleSubmit(successCallback, errorCallback) {
  //   if (this.props.formData.placeId) {
  //     geocodeByPlaceId(this.props.formData.placeId)
  //       .then(results => getLatLng(results[0]))
  //       .then(({ lat, lng }) => {
  //         this.props.onFieldChange('latitude', lat);
  //         this.props.onFieldChange('longitude', lng);
  //         successCallback();
  //       })
  //       .catch(() => {
  //         this.setState({ errors: { location: 'Error finding address. Please try again' } });
  //         errorCallback();
  //       });
  //   }
  //   else {
  //     successCallback();
  //   }
  // }

  render() {
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
              value={this.props.formData.check_in_date}
              onChange={e => this.props.onFieldChange('check_in_date', e.target.value)}
              labelClassName="active"
              error={this.state.errors.check_in_date}
              id="experience-checkin-date"
              name="experience-checkin-date"
              type="date"
            />
            <HelpText s={12}>Enter the check in date for the experience</HelpText>
          </Col>
          <Col s={12} m={6}>
            <Input
              s={12}
              className="with-help timepicker"
              placeholder="14:00"
              label="Check In Time"
              value={this.props.formData.check_in_time}
              onChange={e => this.props.onFieldChange('check_in_time', e.target.value)}
              labelClassName="active"
              error={this.state.errors.check_in_time}
              id="experience-checkin-time"
              name="experience-checkin-time"
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
              value={this.props.formData.check_out_date}
              onChange={e => this.props.onFieldChange('check_out_date', e.target.value)}
              labelClassName="active"
              error={this.state.errors.check_out_date}
              id="experience-checkout-date"
              name="experience-checkout-date"
              type="date"
            />
            <HelpText s={12}>Enter the check out date for the experience</HelpText>
          </Col>
          <Col s={12} m={6}>
            <Input
              s={12}
              className="with-help timepicker"
              placeholder="11:00"
              label="Check Out Time"
              value={this.props.formData.check_out_time}
              onChange={e => this.props.onFieldChange('check_out_time', e.target.value)}
              labelClassName="active"
              error={this.state.errors.check_out_time}
              id="experience-checkout-time"
              name="experience-checkout-time"
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

