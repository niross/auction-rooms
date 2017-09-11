import React, { PropTypes } from 'react';
import { Wizard, WizardStep } from '../../../libs/merlin';

import BasicDetails from './BasicDetails';
import Images from './Images';
import ExtraDetails from './ExtraDetails';

const propTypes = {};
const defaultProps = {};

const initialData = {
  title: '',
  location: '',
  description: '',
  images: []
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

