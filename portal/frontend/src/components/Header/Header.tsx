import React, { useContext } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { AuthContext } from '../../AuthContext';
import { signOut } from 'firebase/auth';
import { auth } from '../../services/firebase';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Avatar,
  Button,
  Box,
  Container,
  Tooltip,
} from '@mui/material';
import { SignOut } from 'phosphor-react';

import DustLogo from '../../assets/Dust_full_logo.png';

import './style.css';

const pages = [
  { name: 'Sobre o Dust', path: '/about' },
  { name: 'Base de Dados', path: '/database' },
  { name: 'Amostras Adversariais', path: '/adversarial' },
  { name: 'Modelo de Defesa', path: '/defense' },
];

const Header: React.FC = () => {
  const { user, setUser } = useContext(AuthContext);
  const location = useLocation();

  const handleSignOut = async () => {
    try {
      await signOut(auth);
      user && setUser(null);
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
    }
  };

  return (
    <AppBar position="static" sx={{ backgroundColor: '#787a81' }}>
      <Container maxWidth="lg">
        <Toolbar
          disableGutters
          sx={{ justifyContent: 'space-evenly', maxHeight: '4vh' }}
        >
          <Link to="/">
            <img
              src={DustLogo}
              alt="Dust Logo"
              className="logo"
              style={{ width: '10rem', height: 'auto' }}
            />
          </Link>
          <Box
            sx={{
              flexGrow: 1,
              display: { xs: 'none', md: 'flex' },
              justifyContent: 'left',
            }}
          >
            {pages.map((page) => (
              <Button
                key={page.name}
                component={Link}
                to={page.path}
                sx={{
                  my: 2,
                  color: location.pathname === page.path ? 'black' : 'white',
                  display: 'block',
                  fontWeight:
                    location.pathname === page.path ? 'bold' : 'normal',
                  pointerEvents:
                    location.pathname === page.path ? 'none' : 'auto',
                }}
              >
                {page.name}
              </Button>
            ))}
          </Box>
          {user && (
            <Box sx={{ flexGrow: 0, display: 'flex', alignItems: 'center' }}>
              <Typography variant="subtitle1" sx={{ marginRight: 2 }}>
                {user.email}
              </Typography>
              <Avatar src={user.photoURL || ''} alt={user.displayName || ''} />
              <Tooltip title="Deslogar">
                <IconButton color="inherit" onClick={handleSignOut}>
                  <SignOut size={32} />
                </IconButton>
              </Tooltip>
            </Box>
          )}
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Header;
