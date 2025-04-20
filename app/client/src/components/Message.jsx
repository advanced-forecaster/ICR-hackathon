import React from 'react';
import './Message.css';

const Message = ({ role, text }) => {
    const isAssistant = role === 'assistant';

    return (
        <div
            className={`message-bubble ${isAssistant ? 'assistant' : 'user'}`}
            style={{
                alignSelf: isAssistant ? 'flex-start' : 'flex-end',
                backgroundColor: isAssistant ? '#e0e0e0' : '#0078d4',
                color: isAssistant ? '#000' : '#fff',
                borderRadius: '15px',
                padding: '10px 15px',
                margin: '5px 0',
                maxWidth: '70%',
            }}
        >
            {text}
        </div>
    );
};

export default Message;