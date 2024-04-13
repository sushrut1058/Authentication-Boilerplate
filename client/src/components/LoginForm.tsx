import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const LoginForm: React.FC = () => {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const auth = useAuth();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    try{
      const response = await fetch('http://localhost:8000/acc/login', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json'
      },
        body: JSON.stringify({ email, password }),
      });
      

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('access', data.access);
        auth.logIn(data.user);
      } else {
        console.log("Can't log in");
      }
    } catch (e){
      console.log(e);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" value={email} onChange={e => setEmail(e.target.value)} />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button type="submit">Log In</button>
    </form>
  );
};

export default LoginForm;