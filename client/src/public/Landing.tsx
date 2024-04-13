import React, { useState } from 'react';
import LoginForm from '../components/LoginForm';
import SignupForm from '../components/SignupForm';


const Landing: React.FC = () => {
  

  return (
    <div>
        <div>
            <LoginForm/>
        </div>
        <div>
            <SignupForm/>
        </div>
    </div>
  );
};

export default Landing;
