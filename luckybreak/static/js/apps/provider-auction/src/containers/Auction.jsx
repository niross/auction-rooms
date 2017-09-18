import React from 'react';
import PropTypes from 'prop-types';
import { Button, Icon } from 'react-materialize';

import { Wizard, WizardStep } from '../../../libs/merlin';
import Schedule from './Schedule';

const propTypes = {
  modalId: PropTypes.string.isRequired,
  experienceId: PropTypes.number,
  buttonFloating: PropTypes.bool,
  buttonWaves: PropTypes.string,
  buttonColour: PropTypes.string,
  buttonId: PropTypes.string.isRequired,
  buttonIcon: PropTypes.string.isRequired,
  buttonText: PropTypes.string.isRequired
};
const defaultProps = {
  experienceId: '',
  buttonFloating: false,
  buttonWaves: 'light',
  buttonColour: 'green'
};

const initialData = {
  check_in: '',
  check_out: '',
  starting_price: '',
  reserve_price: '',
  end_date: ''
};

class Auction extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false
    };
  }

  render() {
    return (
      <Wizard
        id={this.props.modalId}
        ref={wiz => this.wiz = wiz}
        headerText="Add an Auction"
        initialData={Object.assign({ experience: this.props.experienceId }, initialData)}
        className="provider-auction-modal"
        trigger={
          <Button
            id={this.props.buttonId}
            className={this.props.buttonColour}
            floating={this.props.buttonFloating}
            waves={this.props.buttonWaves}
          >
            <Icon left>{this.props.buttonIcon}</Icon>
            {this.props.buttonText}
          </Button>
        }
        onOpen={() => {
        }}
      >
        <WizardStep>
          <Schedule />
        </WizardStep>
        <WizardStep>
          <span>two</span>
        </WizardStep>
        <WizardStep>
          <span>TODO</span>
        </WizardStep>
      </Wizard>
    );
  }
}

Auction.propTypes = propTypes;
Auction.defaultProps = defaultProps;

export default Auction;

