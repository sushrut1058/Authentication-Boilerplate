import React, { useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import EmailVerification from "../components/EmailVerification";
import Onboard from "../components/Onboard";

const HomePage: React.FC = () => {
  
  const auth = useAuth();
  const handleLogout = () => {
    auth.logOut();
  }

  return (
    <div>
    {auth.user.is_onboarded ? 
      
      <h1>Homepage!!!!!!!!!!!!!!!</h1>
      
      :
      (auth.user.is_email_verified ? 
        
          <Onboard/>
         
        :
        
          <EmailVerification/>
        
    )}
    <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default HomePage;
