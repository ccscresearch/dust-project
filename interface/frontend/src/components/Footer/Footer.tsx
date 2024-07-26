import React from 'react';
import { AppBar, Toolbar, Typography, Container } from '@mui/material';

const Footer: React.FC = () => (
  <AppBar position="static" sx={{ backgroundColor: '#787a81' }}>
    <Container maxWidth="lg">
      {' '}
      <Toolbar disableGutters sx={{ justifyContent: 'center' }}>
        <Typography variant="body2" align="center">
          {' '}
          Dust 2024 - Identificando possíveis ataques sem violar a privacidade
          dos pacotes.
        </Typography>
      </Toolbar>
    </Container>
  </AppBar>
);

export default Footer;
