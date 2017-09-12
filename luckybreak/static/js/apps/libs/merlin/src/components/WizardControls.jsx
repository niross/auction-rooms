import React, { PropTypes } from 'react';
import { Row, Col, Button, Preloader, Icon } from 'react-materialize';

const propTypes = {
  loading: PropTypes.bool.isRequired,

  hasSuccessStep: PropTypes.bool,
  currentStep: PropTypes.number.isRequired,
  totalSteps: PropTypes.number.isRequired,

  onForward: PropTypes.func.isRequired,
  forwardButtonText: PropTypes.string,
  forwardButtonIcon: PropTypes.string,
  forwardButtonIconPlacement: PropTypes.oneOf(['left', 'right']),
  forwardButtonClass: PropTypes.string,

  onBack: PropTypes.func.isRequired,

  onCancel: PropTypes.func,
  cancelButtonText: PropTypes.string,

  onComplete: PropTypes.func,
  completeButtonText: PropTypes.string,

  showCancel: PropTypes.bool
};
const defaultProps = {
  hasSuccessStep: true,

  forwardButtonText: 'Next',
  forwardButtonIcon: 'arrow_forward',
  forwardButtonIconPlacement: 'right',
  forwardButtonClass: 'green',

  onCancel: null,
  cancelButtonText: 'Cancel',
  onComplete: null,
  completeButtonText: 'I\'m Done',

  showCancel: false
};

const WizardControls = (props) => {
  const isFirstPage = props.currentStep === 0;
  const isLastPage = props.currentStep === props.totalSteps - 1;
  const showBackButton = ((!isFirstPage && !isLastPage) || (isLastPage && !props.hasSuccessStep))
    && !props.showCancel;

  return (
    <div>
      <Row>
        <Col s={6}>
          {/* Show the cancel button on the first page (if onCancel is provided) */}
          {isFirstPage || props.showCancel ?
            <Button
              waves="light"
              onClick={() => {
                if (props.onCancel) props.onCancel();
              }}
              disabled={props.loading}
              large
              modal="close"
              className="grey lighten-1 grey-text text-darken-4 cancel-button"
            >
              {props.cancelButtonText}
              <Icon left>close</Icon>
            </Button>
            : null}

          {/* If it's not the first page and not the last page show the back button */}
          {showBackButton ?
            <Button
              waves="light"
              onClick={props.onBack}
              disabled={props.loading}
              large
              className="grey lighten-1 grey-text text-darken-4 back-button"
            >
              <Icon left>arrow_back</Icon>
              Back
            </Button>
            : null}
        </Col>
        <Col s={6}>
          {/* If it's the last page and `onComplete` was provded show the close button */}
          {isLastPage && props.onComplete && props.hasSuccessStep ?
            <Button
              waves="light"
              onClick={props.onComplete}
              disabled={props.loading}
              large
              className="green lighten-1 grey-text text-darken-4 complete-button"
            >
              <Icon left>check</Icon>
              {props.completeButtonText}
            </Button>
            : null}

          {/* If it's not the last page show the next button */}
          {!props.hasSuccessStep || !isLastPage ?
            <Button
              waves="light"
              onClick={props.onForward}
              disabled={props.loading}
              large
              className={`${props.forwardButtonClass} next-button`}
            >
              {props.loading ?
                <span><Preloader flashing size="small" />&nbsp;</span>
                : null}
              {props.forwardButtonText}
              {!props.loading ?
                <Icon
                  left={props.forwardButtonIconPlacement === 'left'}
                  right={props.forwardButtonIconPlacement === 'right'}
                >
                  {props.forwardButtonIcon}
                </Icon>
                : null}
            </Button>
            : null}
        </Col>
      </Row>
    </div>
  );
};

WizardControls.propTypes = propTypes;
WizardControls.defaultProps = defaultProps;

export default WizardControls;
