import React from 'react';
import PropTypes from 'prop-types';
import { Row, Col, Input } from 'react-materialize';
import path from 'path';

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
    this.setState({ errors: {}, submissionErrors: {} });
    const form = this.props.formData;
    const data = new FormData();

    // Add standard fields
    const exclude = ['images', 'deleted_images', 'inclusions', 'exclusions'];
    Object.keys(form).forEach((k) => {
      if (exclude.indexOf(k) === -1) data.append(k, this.props.formData[k]);
    });

    // Add inclusions
    if (form.inclusions) form.inclusions.forEach(i => data.append('inclusions', i.name));

    // Add exclusions
    if (form.exclusions) form.exclusions.forEach(e => data.append('exclusions', e.name));

    // Add the default image
    const defaultImage = form.images.find(i => i.default);
    data.append(
      'default_image',
      defaultImage.id ? path.basename(defaultImage.image) : defaultImage.name
    );

    // Add the newly uploaded images
    form.images.filter(i => !i.id).forEach(img => data.append('images', img));

    // Add any deleted images
    form.deleted_images.forEach(img => data.append('deleted_images', img.id));

    if (this.props.formData.id) {
      this.updateExperience(data, successCallback, errorCallback);
    }
    else {
      this.createExperience(data, successCallback, errorCallback);
    }
  }

  createExperience(data, successCallback, errorCallback) {
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

  updateExperience(data, successCallback, errorCallback) {
    makeApiCall(`${apiEndpoints.experiences}${this.props.formData.id}/`, 'PATCH', data, true, null)
      .then((resp) => {
        this.props.onFieldChange('updatedExperience', resp);
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
                value={this.props.formData.inclusions.map(e => e.name).join('\n')}
                onChange={(e) => {
                  const inclusions = [];
                  // Loop through the inclusions
                  e.target.value.split('\n').forEach((exc) => {
                    // Find the existing exclusion
                    const existing = this.props.formData.inclusions.find(i => i.name === exc);
                    // If the exclusion exists already update it
                    if (existing) {
                      existing.name = exc;
                      inclusions.push(existing);
                    }
                    // Otherwise create a new one
                    else {
                      inclusions.push({ name: exc });
                    }
                  });
                  this.props.onFieldChange('inclusions', inclusions);
                }}
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
                value={this.props.formData.exclusions.map(e => e.name).join('\n')}
                onChange={(e) => {
                  const exclusions = [];
                  // Loop through the exclusions
                  e.target.value.split('\n').forEach((exc) => {
                    // Find the existing exclusion
                    const existing = this.props.formData.exclusions.find(i => i.name === exc);
                    // If the exclusion exists already update it
                    if (existing) {
                      existing.name = exc;
                      exclusions.push(existing);
                    }
                    // Otherwise create a new one
                    else {
                      exclusions.push({ name: exc });
                    }
                  });
                  this.props.onFieldChange('exclusions', exclusions);
                }}
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

