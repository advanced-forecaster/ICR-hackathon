import './App.css';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import Message from './components/Message';
import TaskPopup from './components/TaskPopup';
import { useState, useEffect } from 'react';

const localizer = momentLocalizer(moment);

const App = (props) => {
  const [messages, setMessages] = useState([]);
  const [showPopup, setShowPopup] = useState(false);
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedTask, setSelectedTask] = useState('');
  const [events, setEvents] = useState([]);
  const [currentDate, setCurrentDate] = useState(moment());

  useEffect(() => {
    const loadMonthTasks = async () => {
      try {
        const year = currentDate.format('YYYY');
        const month = currentDate.format('MM');
        const response = await fetch(`http://localhost:8000/tasks/month/${year}/${month}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          const tasks = await response.json();
          const newEvents = Object.entries(tasks).map(([date, task]) => ({
            start: moment(date).toDate(),
            end: moment(date).toDate(),
            title: task
          }));
          setEvents(newEvents);
        }
      } catch (error) {
        console.error('Error loading tasks:', error);
      }
    };

    loadMonthTasks();
  }, [currentDate]);

  const handleSelectSlot = (slotInfo) => {
    setSelectedDate(moment(slotInfo.start).format('YYYY-MM-DD'));
    setSelectedTask('');
    setShowPopup(true);
  };

  const handleSelectEvent = (event) => {
    setSelectedDate(moment(event.start).format('YYYY-MM-DD'));
    setSelectedTask(event.title);
    setShowPopup(true);
  };

  const handleSaveTask = async (task) => {
    try {
      const response = await fetch(`http://localhost:8000/tasks/${selectedDate}`, {
        method: selectedTask ? 'PUT' : 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ task }),
      });

      if (!response.ok) {
        throw new Error('Failed to save task');
      }

      const year = currentDate.format('YYYY');
      const month = currentDate.format('MM');
      const tasksResponse = await fetch(`http://localhost:8000/tasks/month/${year}/${month}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (tasksResponse.ok) {
        const tasks = await tasksResponse.json();
        const newEvents = Object.entries(tasks).map(([date, task]) => ({
          start: moment(date).toDate(),
          end: moment(date).toDate(),
          title: task
        }));
        setEvents(newEvents);
      }

      setMessages(prev => [...prev, {
        role: 'assistant',
        text: `Task ${selectedTask ? 'updated' : 'added'} for ${selectedDate}: ${task}`
      }]);
    } catch (error) {
      console.error('Error saving task:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        text: 'Sorry, there was an error saving your task.'
      }]);
    }
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (message) {
      setMessages(prev => [...prev, { role: 'user', text: message }]);
      input.value = '';

      try {
        const response = await fetch('http://localhost:8000/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message })
        });

        if (response.ok) {
          const data = await response.json();
          setMessages(prev => [...prev, {
            role: data.role,
            text: data.text
          }]);
        } else {
          throw new Error('Failed to get response from server');
        }
      } catch (error) {
        console.error('Error in chat:', error);
        setMessages(prev => [...prev, {
          role: 'assistant',
          text: 'Sorry, there was an error processing your message.'
        }]);
      }
    }
  };

  return (
    <div className="App">
      <div className="calendar-container">
        <Calendar
          localizer={localizer}
          events={events}
          startAccessor="start"
          endAccessor="end"
          style={{ height: '100%' }}
          selectable
          onSelectSlot={handleSelectSlot}
          onSelectEvent={handleSelectEvent}
          onNavigate={(date) => setCurrentDate(moment(date))}
        />
      </div>
      {showPopup && (
        <TaskPopup
          date={selectedDate}
          onClose={() => setShowPopup(false)}
          onSave={handleSaveTask}
          initialTask={selectedTask}
        />
      )}
      <div className="chat">
        <div id="messages-box">
          {messages.map((val, index) => (
            <Message key={index} role={val.role} text={val.text} />
          ))}
        </div>
        <form onSubmit={handleChatSubmit}>
          <input id="chat-input" placeholder="Type your message..." />
          <button type="submit">Send</button>
        </form>
      </div>
    </div>
  );
}

export default App;
