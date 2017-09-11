import React, { PropTypes } from 'react';
import { Row, Col, Modal, Button, Icon } from 'react-materialize';
import { Wizard, WizardStep } from './libs/merlin';

const propTypes = {
  header: PropTypes.string.isRequired,
  children: PropTypes.instanceOf(WizardStep),
};
const defaultProps = {};

class ModalWizard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  renderActions() {
    return (
      <Row>
        <Col s={12} m={6}>
          <Button>
            <Icon left>arrow_left</icon> Back
          </Button>
        </Col>
        <Col s={12} m={6}>
          <Button>
            Next <Icon right>arrow_right</icon>
          </Button>
        </Col>
      </Row>
    );
  }

  render() {
    return (
      <Modal
        header="Add an Experience"
        fixedFooter
        actions={this.renderActions()}
        trigger={<Button>Modal testing</Button>}
      >
        <Wizard>
          {this.props.children}
        </Wizard>
      </Modal>
    );
  }
}

ModalWizard.propTypes = propTypes;
ModalWizard.defaultProps = defaultProps;

export default ModalWizard;
