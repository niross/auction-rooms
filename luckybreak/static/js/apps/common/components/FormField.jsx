import React, { PropTypes } from 'react';
import {
  FormGroup, ControlLabel, FormControl, HelpBlock, InputGroup
} from 'react-bootstrap';
import FormInputRequired from './FormInputRequired';

const propTypes = {
  id: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  error: PropTypes.string,
  required: PropTypes.bool,
  onChange: PropTypes.func.isRequired,
  type: PropTypes.string,
  size: PropTypes.oneOf(['sm', 'lg']),
  icon: PropTypes.string,
  placeholder: PropTypes.string,
  helpText: PropTypes.string
};
const defaultProps = {
  value: '',
  error: null,
  required: false,
  type: 'input',
  size: '',
  icon: null,
  placeholder: '',
  helpText: null
};

const FormField = (props) =>
  <FormGroup
    controlId={props.id}
    validationState={props.error == null ? '' : 'error'}
  >
    <ControlLabel>
      {props.label}{props.required ? <FormInputRequired /> : null}
    </ControlLabel>
    <InputGroup bsSize={props.size}>
      <InputGroup.Addon>
        <i className={`fa fa-${props.icon}`} />
      </InputGroup.Addon>
      <FormControl
        type={props.type}
        value={props.value}
        onChange={(e) => props.onChange(e.target.value)}
        placeholder={props.placeholder}
      />
    </InputGroup>
    {props.error ?
      <HelpBlock>{props.error}</HelpBlock>
    : null}
    {props.helpText !== null && !props.error ?
      <HelpBlock>{props.helpText}</HelpBlock>
    : null}
  </FormGroup>;

FormField.propTypes = propTypes;
FormField.defaultProps = defaultProps;

export default FormField;
