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

class ExtraDetails extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      errors: {}
    };
  }

  handleValidate() {
    return true;
  }

  handleSubmit(successCallback, errorCallback) {

    //errorCallback();
  }

  render() {
    return (
      <span>
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
                value={this.props.formData.included}
                onChange={e => this.props.onFieldChange('included', e.target.value)}
                labelClassName="active"
                error={this.state.errors.included}
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
                value={this.props.formData.excluded}
                onChange={e => this.props.onFieldChange('excluded', e.target.value)}
                labelClassName="active"
                error={this.state.errors.excluded}
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
            value={this.props.formData.included}
            onChange={e => this.props.onFieldChange('included', e.target.value)}
            labelClassName="active"
            error={this.state.errors.included}
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

