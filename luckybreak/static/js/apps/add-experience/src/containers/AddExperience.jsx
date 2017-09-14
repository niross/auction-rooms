import React from 'react';
import PropTypes from 'prop-types';
import { Button, Icon } from 'react-materialize';

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
        trigger={
          <Button
            id="add-experience-button"
            className="waves-effect waves-light btn green"
          >
            <Icon left>add</Icon>Add Experience
          </Button>
        }
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
          onCancel={() => window.location.reload()}
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

