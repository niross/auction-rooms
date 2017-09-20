import React from 'react';
import PropTypes from 'prop-types';
import { Modal } from 'react-materialize';

import WizardStep from './WizardStep';
import WizardControls from '../components/WizardControls';
import './main.less';

const propTypes = {
  initialStep: PropTypes.number,
  initialData: PropTypes.object,
  id: PropTypes.string,
  onComplete: PropTypes.func,
  onCancel: PropTypes.func,
  hasSuccessStep: PropTypes.bool,
  headerText: PropTypes.string.isRequired,
  trigger: PropTypes.node.isRequired,
  onOpen: PropTypes.func,
  className: PropTypes.string,
  children: (props, propName) => {
    const prop = props[propName];
    if (!prop || prop.length < 2) {
      return new Error('`Wizard` component requires at least two children');
    }
    let error = null;
    React.Children.forEach(prop, (child) => {
      if (child.type !== WizardStep) {
        error = new Error('`Wizard` children should be of type `WizardStep`');
      }
    });
    return error;
  }
};
const defaultProps = {
  initialStep: 0,
  initialData: {},
  className: '',
  id: 'merlin-wizard',
  hasSuccessStep: true,
  children: null,
  onComplete: null,
  onCancel: null,
  onOpen: null
};

class Wizard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      step: this.props.initialStep,
      loading: false,
      formData: Object.assign({}, this.props.initialData),
      isAuthenticated: false
    };
  }

  getChildren() {
    const children = [];
    this.props.children.forEach((child) => {
      children.push(child);
    });
    return children;
  }

  getVisibleChild(step) {
    // Add an onSuccess callback to the visible child element
    // so we can show the next wizard step on successful submission.
    // Also add the child to refs so we can refer to it later

    // If there are no more steps keep showing the last child
    // and call on complete
    let nextStep = step;
    if (nextStep >= this.getChildren().length) {
      this.handleComplete();
      nextStep -= 1;
    }

    return React.cloneElement(
      this.getChildren()[nextStep], {
        step: nextStep,
        onSuccess: () => this.handleForward(),
        onError: () => this.setState({ loading: false }),
        onComplete: () => this.handleComplete(),
        ref: s => this.visibleNode = s,
        key: `step-${nextStep}`,
        formData: this.state.formData,
        onFieldChange: (fieldName, fieldValue) =>
          this.setState({
            formData: Object.assign(this.state.formData, {
              [fieldName]: fieldValue
            })
          })
      }
    );
  }

  handleCancel() {
    // On modal close reset state
    this.setState({
      step: this.props.initialStep,
      formData: Object.assign({}, this.props.initialData)
    });
    if (this.visibleNode.props.onCancel) this.visibleNode.props.onCancel();
    if (this.props.onCancel) this.props.onCancel();
  }

  /**
   * Call the handleSubmit method of the visible child
   * when the `forward` button is clicked.
   *
   * Here we expect the visible child or it's direct descendent to
   * be of type `WizardStep`.
   */
  handleSubmit() {
    this.setState({ loading: true });
    this.visibleNode.handleSubmit();
  }

  handleForward() {
    this.setState({
      loading: false,
      step: this.state.step + 1
    });
  }

  handleBack() {
    this.setState({
      step: this.state.step - 1
    });
  }

  handleComplete() {
    if (this.props.onComplete) {
      this.props.onComplete();
    }
  }

  renderActions(step) {
    return (
      <WizardControls
        hasSuccessStep={this.props.hasSuccessStep}
        currentStep={this.state.step}
        totalSteps={this.getChildren().length}
        onCancel={step.props.onComplete}
        onComplete={() => this.handleComplete()}
        onForward={() => this.handleSubmit()}
        forwardButtonText={step.props.forwardButtonText}
        forwardButtonIcon={step.props.forwardButtonIcon}
        forwardButtonIconPlacement={step.props.forwardButtonIconPlacement}
        forwardButtonStyle={step.props.forwardButtonStyle}
        onBack={() => this.handleBack()}
        showCancel={step.props.showCancel}
        cancelButtonText={step.props.cancelButtonText}
        disabled={this.getVisibleChild(this.state.step).props.showLoader}
      />
    );
  }

  render() {
    // Clone the direct child and add extra methods for navigation/validation/what have you
    const child = this.getVisibleChild(this.state.step);

    return (
      <Modal
        header={this.props.headerText}
        fixedFooter
        actions={this.renderActions(child)}
        trigger={this.props.trigger}
        id={this.props.id}
        className="merlin"
        modalOptions={{
          complete: () => this.handleCancel(),
          ready: () => {
            if (this.props.onOpen) this.props.onOpen();
          }
        }}
      >
        <span className={this.props.className}>
          {child}
        </span>
      </Modal>
    );
  }
}

Wizard.propTypes = propTypes;
Wizard.defaultProps = defaultProps;

export default Wizard;
