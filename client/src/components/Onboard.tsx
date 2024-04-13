import React, { useEffect, useState } from "react";
import { useAuth } from "../contexts/AuthContext";
import { useNavigate } from "react-router-dom";

const Onboard: React.FC = () => {
  
  const { isAuthenticated, user, isLoading, logOut, updateUser, validateToken } = useAuth(); // Destructure to get isAuthenticated
  const [role, setRole] = useState<string>('');

  if (isLoading){
    return <div>Loading...</div>
  }

  const handleSubmit = async (event : React.FormEvent) => {
    event.preventDefault();

    if(!role){
        alert("Please select a role!");
        return;
    }

    try{
        const token = localStorage.getItem('access');
        
        const response = await fetch('http://localhost:8000/acc/onboard',{
            method: "POST",
            headers:{
              "Content-Type":"application/json",
              Authorization : `Bearer ${token}`
            },
            body:JSON.stringify({role})
        })

        if(response.ok){
            alert("User Onboarded successfully");
            const data = await response.json();
            // const updatedUser = {...user, is_onboarded:true, role:{role}};
            // updateUser(updatedUser);
            validateToken();
        }else{
            const data = await response.json();
            console.log(data.error);
        }
    }catch(error) {
        console.log("Something wrong with resending email:", error)
    }

  }

  console.log()
  return (
    <div>
      <h1>Onboarding Page, Hello: {user.first_name}</h1>
      <form onSubmit={handleSubmit}>
      <label>
        <input
          type="radio"
          value="Hire"
          checked={role === 'Hire'}
          onChange={(e) => setRole(e.target.value)}
        />
        Hire
      </label>
      <label>
        <input
          type="radio"
          value="Hunt"
          checked={role === 'Hunt'}
          onChange={(e) => setRole(e.target.value)}
        />
        Hunt
      </label><br/>
      <button type="submit">Submit</button>
    </form>
      
    </div>
  );
};

export default Onboard;
