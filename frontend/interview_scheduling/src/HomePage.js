import React, {useEffect, useState} from "react";
import {Link} from 'react-router-dom';


const HomePage = ({handleNotification}) => {
    const [slots, setSlots] = useState([]);

    useEffect(()=> {
        const fetchSlots = async()=> {
            try{
                const response = await fetch("http://localhost:8000/slots");
                const data = await response.json();
                setSlots(data);
            }   catch(error){
                handleNotification('Failed to load available slots');
            }
        };
        fetchSlots();
    }, [handleNotification]);

    return(
        <div className="homepage">
            <h2>Available Interview Slots</h2>
            {slots.length == 0?(
                <p>No slots available at the moment. Please check back later.</p>
            ):(
                <ul>
                    {slots.map((slot)=> (
                        <li key={slot.id}>
                            {slot.date} - {slot.time}
                            <Link to="/schedule" state={{slot}} className='schedule-link'></Link>
                        </li>
                    ))}
                </ul>
            )}
            <Link to='/reschedule' className='reschedule-link'>Reschedule Interview</Link>
        </div>
    );
};

export default HomePage;