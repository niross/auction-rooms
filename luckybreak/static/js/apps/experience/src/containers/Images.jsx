import React from 'react';
import PropTypes from 'prop-types';
import { Row, Col, Card, Input, Icon } from 'react-materialize';
import Dropzone from 'react-dropzone';

import { InfoAlert, ErrorAlert, Subheader } from '../../../libs';
import { maxImageSize, maxImageSizeName } from '../../../Config';

const propTypes = {
  formData: PropTypes.object,
  onFieldChange: PropTypes.func
};
const defaultProps = {
  formData: {},
  onFieldChange: () => {}
};

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
    if (files.find(f => f.size > maxImageSize)) {
      this.setState({
        errors: {
          images: `Please ensure all images are less than ${maxImageSizeName} in size.`
        }
      });
      return;
    }
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
              <div style={{ width: '100%' }}>
                <p><strong>Drag &amp; drop images here or click to upload.</strong></p>
                <p>Maximum file size is <strong>7MB</strong>.</p>
                <p>Use <strong>1920x1280</strong> resolution for best results.</p>
              </div>
            </Dropzone>
          </Col>
        </Row>
        {this.props.formData.images && this.props.formData.images.length > 0 ?
          <Row>
            {this.props.formData.images.map(img => (
              <Col
                s={3}
                key={`img-${img.id ? img.id : img.index}`}
              >
                <Card
                  className="image-card"
                  header={
                    <div
                      className="image-preview card-image"
                      style={{ backgroundImage: `url(${img.id ? img.image : img.result})` }}
                    />
                  }
                >
                  <a
                    href="#delete"
                    className="image-delete grey-text text-darken-3"
                    title="Remove this image"
                    onClick={(e) => {
                      e.preventDefault();
                      const formData = this.props.formData;

                      // Add to the deleted images array
                      const deleted = formData.deleted_images;
                      deleted.push(formData.images.find(i => i.id === img.id));
                      this.props.onFieldChange('deleted_images', deleted);

                      // Remove from the images array
                      this.props.onFieldChange('images', formData.images.filter((i) => {
                        if (i.id) return i.id !== img.id;
                        return i !== img;
                      }));
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

