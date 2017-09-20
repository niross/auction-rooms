import React from 'react';
import PropTypes from 'prop-types';
import { Button, Icon } from 'react-materialize';

import { Wizard, WizardStep } from '../../../libs/merlin';
import BasicDetails from './BasicDetails';
import Images from './Images';
import ExtraDetails from './ExtraDetails';
import Success from './Success';
import { makeApiCall } from '../../../libs';
import { apiEndpoints } from '../../../Config';

const propTypes = {
  modalId: PropTypes.string.isRequired,
  experienceId: PropTypes.number,
  buttonFloating: PropTypes.bool,
  buttonWaves: PropTypes.string,
  buttonColour: PropTypes.string,
  buttonId: PropTypes.string.isRequired,
  buttonIcon: PropTypes.string.isRequired,
  buttonText: PropTypes.string.isRequired,
  buttonLarge: PropTypes.bool
};
const defaultProps = {
  experienceId: null,
  buttonFloating: false,
  buttonWaves: 'light',
  buttonColour: 'green',
  buttonLarge: false
};

const initialData = {
  title: '',
  location: '',
  description: '',
  pax_adults: 2,
  pax_children: 0,
  images: [],
  deleted_images: [],
  inclusions: [],
  exclusions: [],
  terms: ''
};

class Experience extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: this.props.experienceId != null
    };
  }

  render() {
    return (
      <Wizard
        id={this.props.modalId}
        ref={wiz => this.wiz = wiz}
        headerText={
          this.props.experienceId ? 'Edit Experience' : 'Add an Experience'
        }
        initialData={initialData}
        className="experience-modal"
        trigger={
          <Button
            id={this.props.buttonId}
            className={`tooltipped ${this.props.buttonColour}`}
            floating={this.props.buttonFloating}
            waves={this.props.buttonWaves}
            fabClickOnly
            large={this.props.buttonLarge}
            data-tooltip={this.props.experienceId ? 'Edit this Experience' : 'Add an Experience'}
            data-position="top"
          >
            <Icon left>{this.props.buttonIcon}</Icon>
            {this.props.buttonText}
          </Button>
        }
        onOpen={() => {
          // When the modal opens fetch the experience data if we are editing
          if (this.props.experienceId) {
            makeApiCall(`${apiEndpoints.experiences}${this.props.experienceId}/`, 'GET')
              .then((resp) => {
                this.wiz.setState({ formData: Object.assign(initialData, resp) });
                this.setState({ loading: false });
              });
          }
        }}
      >
        <WizardStep showLoader={this.state.loading}>
          <BasicDetails />
        </WizardStep>
        <WizardStep>
          <Images />
        </WizardStep>
        <WizardStep>
          <ExtraDetails />
        </WizardStep>
        <WizardStep
          forwardButtonText="Create Auction"
          forwardButtonIcon="add_shopping_cart"
          forwardButtonIconPlacement="left"
          showCancel
          cancelButtonText="Close"
          onCancel={() => window.location.reload()}
        >
          <Success />
        </WizardStep>
      </Wizard>
    );
  }
}

Experience.propTypes = propTypes;
Experience.defaultProps = defaultProps;

export default Experience;

