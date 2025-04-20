import React, { useState } from 'react';
import './TaskPopup.css';

const TaskPopup = ({ date, onClose, onSave, initialTask = '' }) => {
  const [task, setTask] = useState(initialTask);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(task);
    onClose();
  };

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <h2>{initialTask ? 'Edit Task' : 'Add Task'} for {date}</h2>
        <form onSubmit={handleSubmit}>
          <textarea
            value={task}
            onChange={(e) => setTask(e.target.value)}
            placeholder="Enter your task..."
            rows="4"
          />
          <div className="button-group">
            <button type="submit">Save</button>
            <button type="button" onClick={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TaskPopup; 