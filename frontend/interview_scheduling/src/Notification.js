import React, {useEffect, useState} from 'react';


const Notification = ({message, clearMessage})=> {
    const [visible, setVisible] = useState(false);

    useEffect(()=> {
        if (message){
            setVisible(true);
            const timer = setTimeout(()=> {
                setVisible(false);
                clearMessage();
            }, 4000);

            return ()=> clearTimeout(timer);
        }
    }, [message, clearMessage]);

    if(!visible){
        return null;
    }

    return (
        <div className='notification'>
            {message}
        </div>
    );
};

export default Notification;