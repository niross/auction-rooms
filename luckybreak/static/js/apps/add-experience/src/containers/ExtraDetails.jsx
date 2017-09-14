import React from 'react';
import PropTypes from 'prop-types';
import { Row, Col, Input } from 'react-materialize';

import Subheader from '../components/Subheader';
import { HelpText, makeApiCall, WarningAlert } from '../../../libs';
import { apiEndpoints } from '../../../Config';

const propTypes = {
  formData: PropTypes.object,
  onFieldChange: PropTypes.func
};
const defaultProps = {
  formData: {},
  onFieldChange: () => {}
};

class ExtraDetails extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      errors: {},
      submissionErrors: {}
    };
  }

  handleValidate() {
    return true;
  }

  handleSubmit(successCallback, errorCallback) {
    this.setState({ errors: {}, submissionErrors: {} })
    const data = new FormData();

    // Add standard fields
    const exclude = ['images', 'inclusions', 'exclusions'];
    Object.keys(this.props.formData).forEach((k) => {
      if (exclude.indexOf(k) === -1) data.append(k, this.props.formData[k]);
    });

    // Add inclusions
    if (this.props.formData.inclusions) {
      this.props.formData.inclusions.split('\n').forEach(i =>
        data.append('inclusions', i)
      );
    }

    // Add exclusions
    if (this.props.formData.exclusions) {
      this.props.formData.exclusions.split('\n').forEach(i =>
        data.append('exclusions', i)
      );
    }

    // Add the banner image
    const bannerImage = this.props.formData.images.find(i => i.default);
    data.append('banner_image', bannerImage);

    // Add the images
    this.props.formData.images.forEach(img => data.append('images', img));

    // Make the request
    makeApiCall(apiEndpoints.experiences, 'POST', data, true, null)
      .then((resp) => {
        this.props.onFieldChange('savedExperience', resp);
        successCallback();
      })
      .catch((err) => {
        this.setState({ submissionErrors: err.fieldErrors });
        errorCallback();
      });
  }

  render() {
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
        <Subheader text="What's Included" />
        <Row style={{ marginBottom: 0 }}>
          <Col s={6}>
            <Row style={{ marginBottom: 0 }}>
              <Input
                s={12}
                placeholder={
                  'Free WiFi\n' +
                  'Car Parking\n' +
                  'Spa Access'
                }
                className="with-help"
                label="Included Services/Extras"
                type="textarea"
                value={this.props.formData.inclusions}
                onChange={e => this.props.onFieldChange('inclusions', e.target.value)}
                labelClassName="active"
                error={this.state.errors.inclusions}
                id="experience-inclusions"
              />
              <HelpText s={12}>
                List any items or services that <strong>are included</strong> with the experience
              </HelpText>
            </Row>
          </Col>
          <Col s={6}>
            <Row style={{ marginBottom: 0 }}>
              <Input
                s={12}
                placeholder={
                  'Transfers\n' +
                  'Continental Breakfast\n' +
                  'Child Minding'
                }
                className="with-help"
                label="Excluded Services/Extras"
                type="textarea"
                value={this.props.formData.exclusions}
                onChange={e => this.props.onFieldChange('exclusions', e.target.value)}
                labelClassName="active"
                error={this.state.errors.exclusions}
                id="experience-exclusions"
              />
              <HelpText s={12}>
                List any extras or services <strong>not included</strong> in the auction
              </HelpText>
            </Row>
          </Col>
        </Row>
        <Subheader text="The Boring Stuff" />
        <Row style={{ marginBottom: 0 }}>
          <Input
            s={12}
            placeholder={
              'Final auction is non refundable and any dates are final.\n' +
              'Auction is for 2 people sharing one room only.'
            }
            className="with-help"
            label="Terms & Conditions"
            type="textarea"
            value={this.props.formData.terms}
            onChange={e => this.props.onFieldChange('terms', e.target.value)}
            labelClassName="active"
            error={this.state.errors.terms}
            id="experience-terms"
          />
          <HelpText s={12}>
            Optionally enter any terms &amp; conditions you would like attached to
            the auction
          </HelpText>
        </Row>
      </span>
    );
  }
}

ExtraDetails.propTypes = propTypes;
ExtraDetails.defaultProps = defaultProps;

export default ExtraDetails;

