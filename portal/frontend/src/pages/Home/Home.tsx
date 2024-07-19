import React, { useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
import { Box, Button, Typography } from '@mui/material';
import { FcGoogle } from 'react-icons/fc';

import { AuthContext } from '../../AuthContext';
import { auth } from '../../services/firebase';
import DustLogo from '../../assets/Dust_full_logo.png';

const Home: React.FC = () => {
  const { user, setUser } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      navigate('/about');
    }
  }, [user, navigate]);

  const handleGoogleSignIn = async () => {
    const provider = new GoogleAuthProvider();
    try {
      const result = await signInWithPopup(auth, provider);
      setUser(result.user);
    } catch (error) {
      console.error('Erro ao autenticar com o Google:', error);
    }
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      minHeight="100vh"
      px={2}
    >
      <img
        src={DustLogo}
        alt="Dust Logo"
        style={{ maxWidth: '50%', height: 'auto' }}
      />

      <Typography variant="h4" gutterBottom sx={{ color: '#242424', mt: 4 }}>
        Bem-vindo ao Dust!
      </Typography>

      <Button
        variant="contained"
        onClick={handleGoogleSignIn}
        startIcon={<FcGoogle />}
        sx={{ mt: 3, backgroundColor: '#242424', color: 'white' }}
      >
        Entrar com o Google
      </Button>
    </Box>
  );
};

export default Home;
