import React, { PropTypes } from 'react';
import { Wizard, WizardStep } from '../../../libs/merlin';

import BasicDetails from './BasicDetails';
import Images from './Images';
import ExtraDetails from './ExtraDetails';
import Success from './Success';

const propTypes = {};
const defaultProps = {};

const initialData = {
  title: '',
  location: '',
  description: '',
  pax_adults: 2,
  pax_children: 0,
  images: [],
  inclusions: '',
  exclusions: '',
  terms: ''
};

class AddExperience extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <Wizard
        id="add-experience-modal"
        headerText="Add an Experience"
        initialData={initialData}
        triggerId="add-experience-button"
      >
        <WizardStep>
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
        >
          <Success />
        </WizardStep>
        <WizardStep>
          <span>TODO</span>
        </WizardStep>
      </Wizard>
    );
  }
}

AddExperience.propTypes = propTypes;
AddExperience.defaultProps = defaultProps;

export default AddExperience;

