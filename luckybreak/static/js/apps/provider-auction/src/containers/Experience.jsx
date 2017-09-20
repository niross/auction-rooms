import React from 'react';
import PropTypes from 'prop-types';
import { Row, Col, Collection, CollectionItem } from 'react-materialize';

import { HelpText, Subheader, ErrorAlert } from '../../../libs';

const propTypes = {
  formData: PropTypes.object,
  onFieldChange: PropTypes.func,
  experiences: PropTypes.arrayOf(PropTypes.object).isRequired,
  onSkip: PropTypes.func.isRequired,
  initialExperience: PropTypes.number
};
const defaultProps = {
  formData: {},
  onFieldChange: () => {},
  initialExperience: null
};

class Experience extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      errors: {}
    };
  }

  handleValidate() {
    if (!this.props.formData.experience) {
      this.setState({ errors: { experience: 'Please select an experience' } });
      return false;
    }
    return true;
  }

  render() {
    return (
      <span>
        <Subheader text="Experience" />
        <Row>
          <Col s={12} m={8} offset="m2">
            {this.state.errors.experience ?
              <ErrorAlert>{this.state.errors.experience}</ErrorAlert>
              : null}
            <Collection>
              {this.props.experiences.map((exp) => {
                const defaultImage = exp.images.find(i => i.default);
                return (
                  <CollectionItem
                    key={`experience-${exp.id}`}
                    href="#"
                    active={this.props.formData.experience === exp.id}
                    className="avatar valign-wrapper"
                    onClick={() => this.props.onFieldChange('experience', exp.id)}
                  >
                    <img src={defaultImage.image} alt={exp.title} className="circle" />
                    <span className="title">{exp.title}</span>
                    <p>{exp.location}</p>
                  </CollectionItem>
                );
              })}
            </Collection>
            <HelpText s={12}>Select the experience to auction from the list above</HelpText>
          </Col>
        </Row>
      </span>
    );
  }
}

Experience.propTypes = propTypes;
Experience.defaultProps = defaultProps;

export default Experience;

