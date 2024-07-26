import React, { ReactNode } from 'react';
import Header from '../Header/Header';
import Footer from '../Footer/Footer';
import { Box } from '@mui/material';

interface BaseLayoutProps {
  children: ReactNode;
}

const BaseLayout: React.FC<BaseLayoutProps> = ({ children }) => (
  <>
    <Box sx={{ width: '100%', top: 0, zIndex: 10000 }}>
      <Header />
    </Box>

    <Box sx={{ flexGrow: 10 }}>{children}</Box>

    <Box sx={{ mt: 1, position: 'inherit' }}>
      <Footer />
    </Box>
  </>
);

export default BaseLayout;
