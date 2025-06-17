import React, {useState} from 'react';
import {useLocation, useNavigate} from 'react-router-dom';

const ScheduleInterview = ({handleNotification}) => {
    const location = useLocation();
    const navigate = useNavigate();
    const {slot} = location.state || {};

    const [candidateName, setCandidateName] = useState('');
    const [candidateEmail, setCandidateEmail] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async(e)=> {
        e.preventDefault();
        setLoading(true);
        const interviewDetails = {
            name : candidateName,
            email : candidateEmail,
            slotId : slot.id,
        };
        try{
            const response = await fetch("http://localhost:8000/schedule",{
                method : 'POST',
                headers : {
                    'Content-Type':'application/json',
                },
                body : JSON.stringify(interviewDetails),
            });

            if (!response.ok){
                throw new Error("Failed to schedule the interview.");
            }
            const data = await response.json();
            handleNotification(`Interview scheduled successfully for ${data.name} on ${slot.date} at ${slot.time}.`);
            navigate('/');
        }   catch(error){
            handleNotification(error.message);
        }   finally {
            setLoading(false);
        }
    };
    return(
        <div className='schedule-interview'>
            <h2>Schedule Interview</h2>
            {slot? (
                <form onSubmit={handleSubmit}> 
                    <div>
                        <label>Name:</label>
                        <input type='text' value={candidateName} onChange={(e)=> setCandidateName(e.target.value)} required />
                    </div>
                    <div>
                        <label>Email:</label>
                        <input type='email'
                        value={candidateEmail}
                        onChange={(e)=> setCandidateEmail(e.target.value)}
                        required />
                    </div>
                    <div>
                        <p>Selected Slot: {slot.date} at {slot.time}</p>
                    </div>
                    <button type='submit'
                    disabled={loading}>
                        {loading? 'Scheduling...':'Schedule Interview'}
                    </button>
                </form>
            ):(
                <p>No slot Selected. Please select a slot from the home page.</p>
            )}
        </div>
    );
};
export default ScheduleInterview;