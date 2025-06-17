import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './HomePage';
import Notification from './Notification';
import RescheduleInterview from './RescheduleInterview';
import ScheduleInterview from './ScheduleInterview';

function App() {
  const [notification, setNotification] = useState(null);

  const handleNotification = (message) => {
    setNotification(message);
  };

  return (
    <div>
      {notification && <Notification message={notification} />}
      <Routes>
        <Route path='/' element={<HomePage handleNotification={handleNotification} />} />
        <Route path='/schedule' element={<ScheduleInterview handleNotification={handleNotification} />} />
        <Route path='/reschedule' element={<RescheduleInterview handleNotification={handleNotification} />} />
      </Routes>
    </div>
  );
}

export default App;
