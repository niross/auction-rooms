import React from 'react';
import PropTypes from 'prop-types';
import { Button, Icon } from 'react-materialize';

import { Wizard, WizardStep } from '../../../libs/merlin';
import { makeApiCall } from '../../../libs';
import { apiEndpoints } from '../../../Config';
import Experience from './Experience';
import Schedule from './Schedule';
import Pricing from './Pricing';
import Success from './Success';

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
  experienceId: '',
  buttonFloating: false,
  buttonWaves: 'light',
  buttonColour: 'green',
  buttonLarge: false
};

const initialData = {
  check_in: '',
  check_in_date: '',
  check_in_time: '14:00',
  check_out: '',
  check_out_date: '',
  check_out_time: '11:00',
  starting_price: '',
  reserve_price: '',
  duration_days: '7',
  lots: '1'
};

class Auction extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      experiences: []
    };
  }

  renderSteps() {
    // If experience id is added there is no
    // need to include the experience selector
    const steps = [];
    if (!this.props.experienceId) {
      steps.push(
        <WizardStep showLoader={this.state.loading} key="experience">
          <Experience experiences={this.state.experiences} />
        </WizardStep>
      );
    }
    return steps.concat([
      <WizardStep key="schedule">
        <Schedule />
      </WizardStep>,
      <WizardStep key="pricing">
        <Pricing />
      </WizardStep>,
      <WizardStep
        key="success"
        forwardButtonText="Create Auction"
        forwardButtonIcon="add_shopping_cart"
        forwardButtonIconPlacement="left"
      >
        <Success />
      </WizardStep>
    ]);
  }

  render() {
    return (
      <Wizard
        id={this.props.modalId}
        ref={wiz => this.wiz = wiz}
        headerText="Add an Auction"
        initialData={Object.assign({ experience: this.props.experienceId }, initialData)}
        className="provider-auction-modal"
        onComplete={() => window.location.reload()}
        trigger={
          <Button
            id={this.props.buttonId}
            className={`tooltipped ${this.props.buttonColour}`}
            floating={this.props.buttonFloating}
            waves={this.props.buttonWaves}
            fabClickOnly
            large={this.props.buttonLarge}
            data-tooltip={this.props.experienceId ?
              'Create an auction for this experience' : 'Add an auction'
            }
            data-position="top"
          >
            <Icon left>{this.props.buttonIcon}</Icon>
            {this.props.buttonText}
          </Button>
        }
        onOpen={() => {
          makeApiCall(`${apiEndpoints.experiences}`, 'GET')
            .then((resp) => {
              this.setState({ loading: false, experiences: resp });
            });
        }}
      >
        {this.renderSteps()}
      </Wizard>
    );
  }
}

Auction.propTypes = propTypes;
Auction.defaultProps = defaultProps;

export default Auction;

