import React from 'react';
import PropTypes from 'prop-types';
import { Row, Col, Input } from 'react-materialize';
import { geocodeByPlaceId, getLatLng } from 'react-places-autocomplete';

import Subheader from '../components/Subheader';
import { LocationAutocomplete, HelpText } from '../../../libs';

const propTypes = {
  formData: PropTypes.object,
  onFieldChange: PropTypes.func
};
const defaultProps = {
  formData: {},
  onFieldChange: () => {}
};

class BasicDetails extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      errors: {}
    };
    this.requiredFields = ['title', 'location', 'description'];
  }

  handleValidate() {
    const errors = {};
    const form = this.props.formData;
    if (!form.placeId) {
      errors.location = 'Please select a valid location';
    }
    if (form.pax_adults === 0 && form.pax_children === 0) {
      errors.pax_adults = 'An adult or child is required';
      errors.pax_children = 'An adult or child is required';
    }
    this.setState({ errors });
    return Object.keys(errors).length === 0;
  }

  handleSubmit(successCallback, errorCallback) {
    geocodeByPlaceId(this.props.formData.placeId)
      .then(results => getLatLng(results[0]))
      .then(({ lat, lng }) => {
        this.props.onFieldChange('latitude', lat);
        this.props.onFieldChange('longitude', lng);
        successCallback();
      })
      .catch(() => {
        this.setState({ errors: { location: 'Error finding address. Please try again' } });
        errorCallback();
      });
  }

  render() {
    return (
      <span>
        <Subheader text="Basic Details" />
        <Row>
          <Col s={12}>
            <Input
              s={12}
              className="with-help"
              placeholder="Penthouse Apartment in Central London"
              label="Title"
              value={this.props.formData.title}
              onChange={e => this.props.onFieldChange('title', e.target.value)}
              labelClassName="active"
              error={this.state.errors.title}
              id="experience-title"
            />
            <HelpText s={12}>Enter an eye catching title for your experience</HelpText>
          </Col>
          <Col s={12}>
            <LocationAutocomplete
              label="Location"
              value={this.props.formData.location}
              placeholder="Start typing the location of your experience"
              id="experience-location"
              onChange={val => this.props.onFieldChange('location', val)}
              onSelect={(address, placeId) => {
                this.props.onFieldChange('location', address);
                this.props.onFieldChange('placeId', placeId);
              }}
              helpText="Enter the address for your experience"
              error={this.state.errors.location}
              s={12}
            />
          </Col>
          <Col s={6}>
            <Input
              s={12}
              className="with-help"
              label="Number of Adults"
              value={this.props.formData.pax_adults.toString()}
              onChange={e => this.props.onFieldChange('pax_adults', parseInt(e.target.value, 10))}
              labelClassName="active"
              error={this.state.errors.pax_adults}
              type="number"
              min={0}
              id="experience-pax-adults"
            />
            <HelpText s={12}>How many adults can the experience accommodate</HelpText>
          </Col>
          <Col s={6}>
            <Input
              s={12}
              className="with-help"
              label="Number of Children"
              value={this.props.formData.pax_children.toString()}
              onChange={e => this.props.onFieldChange('pax_children', parseInt(e.target.value, 10))}
              labelClassName="active"
              error={this.state.errors.pax_children}
              type="number"
              min={0}
              id="experience-pax-children"
            />
            <HelpText s={12}>How many children can the experience accommodate</HelpText>
          </Col>
          <Col s={12}>
            <Input
              s={12}
              placeholder={
                'Stunning apartment perfect for a romantic getaway for two.\n\n' +
                'Price includes a free bottle of bubbly and full use of the spa.'
              }
              className="with-help"
              label="About the Experience"
              type="textarea"
              value={this.props.formData.description}
              onChange={e => this.props.onFieldChange('description', e.target.value)}
              labelClassName="active"
              error={this.state.errors.description}
              id="experience-description"
            />
            <HelpText s={12}>Sell the experience to your prospective guests</HelpText>
          </Col>
        </Row>
      </span>
    );
  }
}

BasicDetails.propTypes = propTypes;
BasicDetails.defaultProps = defaultProps;

export default BasicDetails;

