import React, { PropTypes } from 'react';
import { Row, Col, Input } from 'react-materialize';

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
    if (!this.props.formData.placeId) {
      errors.location = 'Please select a valid location';
    }
    this.setState({ errors });
    return Object.keys(errors).length === 0;
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
            />
            <HelpText s={12}>Enter an eye catching title for your experience</HelpText>
          </Col>
          <Col s={12}>
            <LocationAutocomplete
              label="Location"
              value={this.props.formData.location}
              placeholder="Start typing the location of your experience"
              id="location"
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

