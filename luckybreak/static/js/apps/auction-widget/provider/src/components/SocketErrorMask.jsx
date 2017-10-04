import React from 'react';
import { Button, Icon } from 'react-materialize';

const propTypes = {};
const defaultProps = {};

const SocketErrorMask = () => (
  <div className="socket-error-mask">
    <div>
      <p>Error Syncing Auction!</p>
      <p>Attempting to reconnect...</p>
      <p>Click reload if the problem persists</p>
      <br />
      <p>
        <Button
          className="btn grey lighten-2 grey-text text-darken-3"
          onClick={() => window.location.reload()}
        >
          <Icon left>refresh</Icon>Reload Now
        </Button>
      </p>
    </div>
  </div>
);

SocketErrorMask.propTypes = propTypes;
SocketErrorMask.defaultProps = defaultProps;

export default SocketErrorMask;
