import React from 'react';
import PropTypes from 'prop-types';

import WizardLoading from '../components/WizardLoading';

const propTypes = {
  loading: PropTypes.bool,
  onFieldChange: PropTypes.func,
  onSuccess: PropTypes.func,
  onComplete: PropTypes.func,
  onCancel: PropTypes.func,
  onError: PropTypes.func,
  formData: PropTypes.object,
  showLoader: PropTypes.bool,
  children: PropTypes.element.isRequired
};
const defaultProps = {
  loading: false,
  onFieldChange: () => {},
  onSuccess: () => {},
  onComplete: () => {},
  onCancel: () => {},
  onError: () => {},
  formData: {},
  showLoader: false
};

class WizardStep extends React.Component {
  /**
   * Add extra props to the visible child before it is mounted
   */
  getChildForm() {
    const form = React.cloneElement(
      this.props.children, {
        ref: s => this.form = s,
        loading: this.props.loading,
        onFieldChange: (name, value) => this.props.onFieldChange(name, value),
        onComplete: () => this.props.onComplete(),
        onCancel: () => this.props.onCancel(),
        formData: this.props.formData,
        onError: () => this.props.onError(),
        onSkip: () => this.props.onSuccess(),
        onSubmit: () => this.handleSubmit()
      }
    );
    return form;
  }

  /**
   * If the child has required fields make sure they are populated
   * If the child has a validate function and it passes return true.
   * If it fails fire the onError callback and return false.
   * If no callback exists return true.
   */
  isValid() {
    if (this.form.requiredFields) {
      const errors = {};
      this.form.requiredFields.forEach((f) => {
        const field = this.props.formData[f];
        if (field == null || field === '') {
          errors[f] = 'This field is required';
        }
      });
      this.form.setState({ errors });
      if (Object.keys(errors).length > 0) {
        this.props.onError();
        return false;
      }
    }

    if (this.form.handleValidate) {
      if (this.form.handleValidate()) {
        return true;
      }
      this.props.onError();
      return false;
    }
    return true;
  }

  /**
   * When the form is submitted check it is valid.
   * If it is valid call the `onSubmit` callback.
   * Passes the onSucess callback to move the wizard on to the next step
   *
   * If `handleSubmit` is not defined, the form is not required so
   * just call `onSuccess`
   */
  handleSubmit() {
    if (this.isValid()) {
      if (this.form.handleSubmit) {
        this.form.handleSubmit(this.props.onSuccess, this.props.onError);
      }
      else {
        this.props.onSuccess();
      }
    }
  }


  render() {
    return (
      <div className="wizard-step">
        {this.props.showLoader ?
          <WizardLoading />
          : this.getChildForm()}
      </div>
    );
  }
}

WizardStep.propTypes = propTypes;
WizardStep.defaultProps = defaultProps;

export default WizardStep;

