import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
  Menu,
  MenuItem
} from '@mui/material'
import { AccountCircle, Menu as MenuIcon } from '@mui/icons-material'
import { useAuth } from '../../contexts/AuthContext'

const Navbar = () => {
  const { user, logout, isAuthenticated, isAdmin } = useAuth()
  const navigate = useNavigate()
  const [anchorEl, setAnchorEl] = React.useState(null)

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget)
  }

  const handleClose = () => {
    setAnchorEl(null)
  }

  const handleLogout = () => {
    logout()
    handleClose()
    navigate('/')
  }

  return (
    <AppBar
      position="sticky"
      elevation={0}
      sx={{
        backgroundColor: 'white',
        borderBottom: '1px solid',
        borderColor: 'divider',
        boxShadow: '0 2px 8px rgba(0,0,0,0.05)',
      }}
    >
      <Toolbar sx={{ px: { xs: 2, sm: 3 }, py: 2 }}>
        <Typography
          variant="h5"
          component={Link}
          to="/"
          sx={{
            flexGrow: { xs: 1, md: 0 },
            textDecoration: 'none',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            fontWeight: 700,
            mr: { md: 6 },
            fontSize: { xs: '1.25rem', sm: '1.5rem' },
          }}
        >
          NewsHub
        </Typography>
        <Box
          sx={{
            display: { xs: 'none', md: 'flex' },
            gap: 1,
            flexGrow: 1,
            ml: 4,
          }}
        >
          {isAuthenticated ? (
            <>
              {isAdmin && (
                <Button
                  component={Link}
                  to="/admin"
                  sx={{
                    color: 'text.primary',
                    fontWeight: 500,
                    textTransform: 'none',
                    '&:hover': {
                      backgroundColor: 'action.hover',
                      color: 'primary.main',
                    },
                  }}
                >
                  Admin
                </Button>
              )}
              <Button
                component={Link}
                to="/recommendations"
                sx={{
                  color: 'text.primary',
                  fontWeight: 500,
                  textTransform: 'none',
                  '&:hover': {
                    backgroundColor: 'action.hover',
                    color: 'primary.main',
                  },
                }}
              >
                Recommendations
              </Button>
              <Button
                component={Link}
                to="/saved"
                sx={{
                  color: 'text.primary',
                  fontWeight: 500,
                  textTransform: 'none',
                  '&:hover': {
                    backgroundColor: 'action.hover',
                    color: 'primary.main',
                  },
                }}
              >
                Saved
              </Button>
            </>
          ) : null}
        </Box>
        <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
          {isAuthenticated ? (
            <>
              <Button
                component={Link}
                to="/subscription"
                variant="outlined"
                sx={{
                  borderColor: 'primary.main',
                  color: 'primary.main',
                  textTransform: 'none',
                  fontWeight: 600,
                  borderRadius: 3,
                  px: 3,
                  display: { xs: 'none', sm: 'flex' },
                  '&:hover': {
                    borderColor: 'primary.dark',
                    backgroundColor: 'primary.light',
                    backgroundColor: 'rgba(26, 115, 232, 0.08)',
                  },
                }}
              >
                Subscribe
              </Button>
              <IconButton
                size="large"
                edge="end"
                onClick={handleMenu}
                sx={{
                  color: 'text.primary',
                  backgroundColor: 'action.hover',
                  '&:hover': {
                    backgroundColor: 'action.selected',
                  },
                }}
              >
                <AccountCircle />
              </IconButton>
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleClose}
                PaperProps={{
                  elevation: 8,
                  sx: {
                    mt: 1.5,
                    borderRadius: 2,
                    minWidth: 180,
                    boxShadow: '0 8px 24px rgba(0,0,0,0.12)',
                  },
                }}
              >
                <MenuItem
                  component={Link}
                  to="/profile"
                  onClick={handleClose}
                  sx={{
                    '&:hover': {
                      backgroundColor: 'action.hover',
                    },
                  }}
                >
                  Profile
                </MenuItem>
                <MenuItem
                  onClick={handleLogout}
                  sx={{
                    '&:hover': {
                      backgroundColor: 'action.hover',
                    },
                  }}
                >
                  Logout
                </MenuItem>
              </Menu>
            </>
          ) : (
            <>
              <Button
                component={Link}
                to="/login"
                sx={{
                  color: 'text.primary',
                  fontWeight: 500,
                  textTransform: 'none',
                  '&:hover': {
                    backgroundColor: 'action.hover',
                  },
                }}
              >
                Login
              </Button>
              <Button
                component={Link}
                to="/register"
                variant="contained"
                sx={{
                  textTransform: 'none',
                  fontWeight: 600,
                  borderRadius: 3,
                  px: 3,
                  boxShadow: '0 2px 8px rgba(26, 115, 232, 0.3)',
                }}
              >
                Sign Up
              </Button>
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  )
}

export default Navbar

