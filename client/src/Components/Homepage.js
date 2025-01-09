import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {

    return (
        <div className='main'>
            <div className="main-page">
                <img className='main-image' src='rgukt-logo.jpeg' alt='RGUKT Logo'></img>
                <div className='homepage'>
                    <h1 className="headline">Welcome to RGUKT BASAR Admissions 2024-2025</h1>
                </div>
                
            </div>
            <div className='content'>
                <div>
                    <p>The journey to college is an exciting step toward shaping your future. At RGUKT Basar, we believe in unlocking your potential, fostering growth, and empowering you to achieve your dreams. The path may be challenging, but every step brings you closer to success. Your future starts here.</p>
                    <Link to='/apply'><button>Apply Now</button></Link>
                </div>
                <img className='hemo-image' src='hemoimage.svg' alt='Hemo Image'></img>
            </div>
            
        </div>
    );
};

export default HomePage;
