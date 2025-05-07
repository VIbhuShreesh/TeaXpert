import React from 'react';
import { Box, Typography, Container } from '@mui/material';
import { styled } from '@mui/material/styles';

const StyledFooter = styled(Box)(({ theme }) => ({
  backgroundColor: theme.palette.primary.main,
  color: 'white',
  padding: theme.spacing(3),
  marginTop: 'auto',
}));

function Footer() {
  return (
    <StyledFooter>
      <Container maxWidth="lg">
        <Box sx={{ textAlign: 'center' }}>
          <Typography variant="body1">
            © {new Date().getFullYear()} TeaXpert - Tea Leaf Disease Detection System
          </Typography>
          <Typography variant="body2" sx={{ mt: 1 }}>
            Developed with ❤️ for tea farmers
          </Typography>
        </Box>
      </Container>
    </StyledFooter>
  );
}

export default Footer; 