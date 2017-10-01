import React from 'react';
import PropTypes from 'prop-types';
import Lightbox from 'react-images';
import { Row, Col } from 'react-materialize';

const propTypes = {
  images: PropTypes.arrayOf(PropTypes.shape({
    src: PropTypes.string,
    thumb: PropTypes.string
  })).isRequired
};
const defaultProps = {};

class Gallery extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isOpen: false,
      currentImageIndex: 0
    };
  }
  render() {
    return (
      <Row className="gallery">
        <Col s={12} className="thumbs">
          {this.props.images.map((img, idx) => (
            <span
              role="button"
              tabIndex={0}
              onClick={() =>
                this.setState({ isOpen: true, currentImageIndex: idx })
              }
            >
              <img
                className="thumb"
                src={img.thumb}
                alt=""
              />
            </span>
          ))}
        </Col>
        <Lightbox
          isOpen={this.state.isOpen}
          onClose={() => this.setState({ isOpen: false })}
          images={this.props.images.map(i => ({
            src: i.src,
            thumbnail: i.thumb
          }))}
          currentImage={this.state.currentImageIndex}
          showThumbnails
          backdropClosesModal
          onClickNext={() =>
            this.setState({ currentImageIndex: this.state.currentImageIndex + 1 })
          }
          onClickPrev={() =>
            this.setState({ currentImageIndex: this.state.currentImageIndex - 1 })
          }
          onClickThumbnail={i => this.setState({ currentImageIndex: i })}
        />
      </Row>
    );
  }
}

Gallery.propTypes = propTypes;
Gallery.defaultProps = defaultProps;

export default Gallery;
