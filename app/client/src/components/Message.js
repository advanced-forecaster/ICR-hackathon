import React from 'react';
import './Message.css';

const Message = ({ role, text }) => {
  return (
    <div className={`message ${role}`}>
      <div className="message-role">{role}</div>
      <div className="message-content">{text}</div>
    </div>
  );
};

export default Message; 