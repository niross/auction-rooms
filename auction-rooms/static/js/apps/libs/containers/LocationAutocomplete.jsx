import React from 'react';
import PropTypes from 'prop-types';
import { Col } from 'react-materialize';
import PlacesAutocomplete from 'react-places-autocomplete';

import HelpText from '../components/HelpText';

const propTypes = {
  label: PropTypes.string.isRequired,
  value: PropTypes.string,
  placeholder: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  onSelect: PropTypes.func.isRequired,
  helpText: PropTypes.string.isRequired,
  error: PropTypes.string,
  s: PropTypes.number,
  m: PropTypes.number,
  l: PropTypes.number
};
const defaultProps = {
  value: '',
  error: null,
  s: 12,
  m: null,
  l: null
};

class LocationAutocomplete extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      valid: props.value != null
    };
  }

  render() {
    return (
      <span>
        <Col className={`input-field s${this.props.s} m${this.props.m} l${this.props.l}`}>
          <PlacesAutocomplete
            ref={pa => this.autocomplete = pa}
            inputProps={{
              onChange: (val) => {
                this.props.onChange(val);
                this.setState({ valid: false });
              },
              placeholder: this.props.placeholder,
              id: this.props.id,
              name: this.props.name,
              value: this.props.value,
              onBlur: () => {
                if (!this.state.valid) {
                  this.props.onChange('');
                }
              }
            }}
            onSelect={(address, placeId) => {
              this.setState({ valid: !!placeId });
              this.props.onSelect(address, placeId);
            }}
            classNames={{
              input: `autocomplete with-help${this.props.error ? ' invalid' : ''}`
            }}
            styles={{
              input: { padding: 0 },
              root: { zIndex: 2 }
            }}
          />
          <label htmlFor={this.props.id} className="active">
            {this.props.label}
          </label>
        </Col>
        {this.props.error ?
          <div className={`col s${this.props.s} m${this.props.m} l${this.props.l} input-error`}>
            {this.props.error}
          </div>
          : null}
        <HelpText
          style={{ marginTop: this.props.error ? '-18px' : '0' }}
          s={this.props.s}
          m={this.props.m}
          l={this.props.l}
        >
          {this.props.helpText}
        </HelpText>
      </span>
    );
  }
}


LocationAutocomplete.propTypes = propTypes;
LocationAutocomplete.defaultProps = defaultProps;

export default LocationAutocomplete;

