import React, { PropTypes } from 'react';
import { Row, Col, Card, Input, Icon } from 'react-materialize';
import Dropzone from 'react-dropzone';

import Subheader from '../components/Subheader';
import { InfoAlert, ErrorAlert } from '../../../libs';

const propTypes = {
  formData: PropTypes.object.isRequired,
  onFieldChange: PropTypes.func.isRequired
};
const defaultProps = {};

class BasicDetails extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      errors: {}
    };
  }

  componentWillUnmount() {
    if (this.props.formData.images) {
      this.props.formData.images.forEach(img =>
        window.URL.revokeObjectURL(img.preview)
      );
    }
  }

  onDrop(files) {
    this.setState({ errors: {} });
    files.forEach((file) => {
      const reader = new FileReader();
      const img = file;
      reader.onload = () => {
        img.result = reader.result;
        img.index = this.props.formData.images.length;
        if (img.index === 0) img.default = true;
        this.props.onFieldChange(
          'images', this.props.formData.images.concat([img])
        );
      };
      reader.readAsDataURL(file);
    });
  }

  handleValidate() {
    const errors = {};
    const images = this.props.formData.images;
    if (images.length === 0) {
      errors.images = 'Please upload at least one image for your experience';
    }
    if (!images.find(img => img.default === true)) {
      errors.images = 'Please choose a default image for your experience';
    }
    this.setState({ errors });
    return Object.keys(errors).length === 0;
  }

  render() {
    return (
      <span>
        <Subheader text="Images" />
        {this.state.errors.images ?
          <ErrorAlert>{this.state.errors.images}</ErrorAlert>
          : null}
        <Row>
          <Col s={12}>
            <Dropzone
              className="dropzone valign-wrapper"
              multiple
              accept="image/jpeg, image/png"
              onDrop={files => this.onDrop(files)}
            >
              <p>Drag &amp; drop images here or click to upload</p>
            </Dropzone>
          </Col>
        </Row>
        {this.props.formData.images && this.props.formData.images.length > 0 ?
          <Row>
            {this.props.formData.images.map(img => (
              <Col
                s={3}
                key={`img-${img.index}`}
              >
                <Card
                  className="image-card"
                  header={
                    <div
                      className="image-preview card-image"
                      style={{ backgroundImage: `url(${img.result})` }}
                    />
                  }
                >
                  <a
                    href="#delete"
                    className="image-delete grey-text text-darken-3"
                    title="Remove this image"
                    onClick={(e) => {
                      e.preventDefault();
                      this.props.onFieldChange('images', this.props.formData.images.filter(
                        i => i !== img
                      ));
                    }}
                  >
                    <Icon tiny>cancel</Icon>
                  </a>
                  <Row title="The default image will be used as the auction background image.">
                    <Input
                      s={12}
                      name="group1"
                      type="checkbox"
                      value="default"
                      label="Default"
                      checked={img.default}
                      onChange={(e) => {
                        const images = [];
                        this.props.formData.images.forEach((i) => {
                          const image = i;
                          image.default = false;
                          if (image === img) image.default = e.target.checked;
                          images.push(image);
                        });
                        this.props.onFieldChange('images', images);
                      }}
                    />
                  </Row>
                </Card>
              </Col>
            ))}
          </Row>
          :
          <Row>
            <Col s={12}>
              <InfoAlert>
                Upload one or more images of your experience.
              </InfoAlert>
            </Col>
          </Row>
        }
      </span>
    );
  }
}

BasicDetails.propTypes = propTypes;
BasicDetails.defaultProps = defaultProps;

export default BasicDetails;

