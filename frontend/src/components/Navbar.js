import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { styled } from '@mui/material/styles';

const StyledAppBar = styled(AppBar)(({ theme }) => ({
  backgroundColor: theme.palette.primary.main,
  boxShadow: 'none',
}));

const NavButton = styled(Button)(({ theme }) => ({
  color: 'white',
  marginLeft: theme.spacing(2),
  '&:hover': {
    backgroundColor: theme.palette.primary.dark,
  },
}));

function Navbar() {
  return (
    <StyledAppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          TeaXpert
        </Typography>
        <Box>
          <NavButton>Home</NavButton>
          <NavButton>About</NavButton>
          <NavButton>Contact</NavButton>
        </Box>
      </Toolbar>
    </StyledAppBar>
  );
}

export default Navbar; 