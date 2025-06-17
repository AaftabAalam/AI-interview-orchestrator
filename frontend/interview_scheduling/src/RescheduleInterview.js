import React, {useEffect, useState} from "react";
import {Link} from 'react-router-dom';

const RescheduleInterview = ({handleNotification}) => {
    const [interviews, setInterviews] = useState([]);
    const [selectedInterview, setSelectedInterview] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(()=> {
        const fetchInterviews = async()=> {
            try{
                const response = await fetch("http://localhost:8000/interviews");
                const data = await response.json();
                setInterviews(data);
            }   catch(error){
                handleNotification("Failed to load scheduled interviews.");
            }
        };
        fetchInterviews();
    }, [handleNotification]);

    const handleReschedule = async (interview)=> {
        setLoading(true);
        setSelectedInterview(interview);
        try{
            const response = await fetch("http://localhost:8000/slots");
            const slots = await response.json();
            setSelectedInterview({...interview, availableSlots: slots});
        }   catch(error){
            handleNotification("Failed to load available slots.");
        }   finally{
            setLoading(false);
        }
    };

    const confirmReschedule = async (newSlot)=> {
        setLoading(true);
        const rescheduleDetails = {
            interviewId : selectedInterview.id,
            newSlotId : newSlot.id,
        };
        try{
            const response = await fetch("http://localhost:8000/reschedule",{
                method : 'POST',
                headers : {
                    'Content-Type' : 'application/json',
                },
                body: JSON.stringify(rescheduleDetails),
            });

            if (!response.ok){
                throw new Error("Failed to reschedule the interview.");
            }

            const data = await response.json();
            handleNotification(`Interview rescheduled to ${data.newDate} at ${data.newTime}.`);
            setInterviews(interviews.map(interview=> interview.id === selectedInterview.id? {...interview, ...data}: interview));
            setSelectedInterview(null);
        }   catch(error){
            handleNotification(error.message);
        }   finally{
            setLoading(false);
        }
    };

    return(
        <div className="reschedule-interview">
            <h2>Reschedule Interview</h2>
            {loading && <p>Loading...</p>}
            {interviews.length === 0? (
                <p>
                    No interviews scheduled. Please schedule an interview first.
                </p>
            ):(
                <ul>
                    {interviews.map((interview)=> (
                        <li key={interview.id}>
                            {interview.name} - {interview.date} at {interview.time}
                            <button onClick={()=> handleReschedule(interview)}>Reschedule</button>
                        </li>
                    ))}
                </ul>
            )}
            {selectedInterview && (
                <div className="available-slots">
                    <h3>Available Slots For Rescheduling</h3>
                    {selectedInterview.availableSlots && selectedInterview.availableSlots.length > 0 ? (
                        <ul>
                            {selectedInterview.availableSlots.map((slot)=> (
                                <li key={slot.id}>
                                    {slot.date} at {slot.time}
                                    <button onClick={()=> confirmReschedule(slot)}>Confirm Reschedule</button>
                                </li>
                            ))}
                        </ul>
                    ):(
                        <p>No slots available for rescheduling.</p>
                    )}
                    <button onClick={()=> setSelectedInterview(null)}>Cancel</button>
                </div>
            )}
        </div>
    );
};

export default RescheduleInterview;