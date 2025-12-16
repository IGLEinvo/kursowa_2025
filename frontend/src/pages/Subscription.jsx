import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Alert,
  Chip,
  CircularProgress,
  Paper,
  Divider
} from '@mui/material'
import { Check, Star } from '@mui/icons-material'
import { subscriptionsApi } from '../api/api'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'
import { format } from 'date-fns'

const Subscription = () => {
  const { isAuthenticated } = useAuth()
  const navigate = useNavigate()
  const [tiers, setTiers] = useState([])
  const [currentSubscription, setCurrentSubscription] = useState(null)
  const [loading, setLoading] = useState(true)
  const [subscribing, setSubscribing] = useState(null)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login')
      return
    }
    fetchTiers()
    fetchCurrentSubscription()
  }, [isAuthenticated, navigate])

  const fetchTiers = async () => {
    try {
      setLoading(true)
      const response = await subscriptionsApi.getTiers()
      if (response.data && response.data.tiers) {
        // Filter out free tier and show only paid options
        const paidTiers = response.data.tiers.filter(tier => tier.type !== 'free')
        setTiers(paidTiers)
      }
    } catch (error) {
      console.error('Failed to fetch subscription tiers:', error)
      setError('Failed to load subscription plans. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const fetchCurrentSubscription = async () => {
    try {
      const response = await subscriptionsApi.getUserSubscription()
      if (response.data && response.data.subscription) {
        setCurrentSubscription(response.data.subscription)
      }
    } catch (error) {
      console.error('Failed to fetch current subscription:', error)
    }
  }

  const handleSubscribe = async (tierId, tierName) => {
    if (!isAuthenticated) {
      navigate('/login')
      return
    }

    try {
      setSubscribing(tierId)
      setError(null)
      setSuccess(null)

      const response = await subscriptionsApi.createSubscription(tierId)
      
      if (response.data && response.data.subscription) {
        setSuccess(`Successfully subscribed to ${tierName}!`)
        // Refresh subscription info
        await fetchCurrentSubscription()
        // Reload page after 2 seconds to refresh premium status
        setTimeout(() => {
          window.location.reload()
        }, 2000)
      }
    } catch (error) {
      console.error('Failed to subscribe:', error)
      const errorMsg = error.response?.data?.error || error.message || 'Failed to subscribe. Please try again.'
      setError(errorMsg)
    } finally {
      setSubscribing(null)
    }
  }

  if (!isAuthenticated) {
    return null
  }

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '400px' }}>
        <CircularProgress />
      </Box>
    )
  }

  const hasActivePremium = currentSubscription && 
    ['paid', 'student', 'corporate'].includes(currentSubscription.tier_type) &&
    new Date(currentSubscription.end_date) > new Date()

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Premium Subscriptions
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Unlock premium content, ad-free experience, and exclusive articles
      </Typography>

      {hasActivePremium && (
        <Alert severity="success" sx={{ mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            You have an active {currentSubscription.tier_name} subscription
          </Typography>
          <Typography variant="body2">
            Expires: {format(new Date(currentSubscription.end_date), 'MMMM d, yyyy')}
          </Typography>
        </Alert>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 3 }} onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      <Grid container spacing={3} sx={{ mt: 2 }}>
        {tiers.map((tier) => {
          const isCurrentTier = currentSubscription && 
            currentSubscription.tier_type === tier.type &&
            new Date(currentSubscription.end_date) > new Date()
          
          const features = tier.features ? (
            typeof tier.features === 'string' ? JSON.parse(tier.features) : tier.features
          ) : {}

          return (
            <Grid item xs={12} md={4} key={tier.id}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  position: 'relative',
                  border: isCurrentTier ? 2 : 1,
                  borderColor: isCurrentTier ? 'primary.main' : 'divider'
                }}
              >
                {isCurrentTier && (
                  <Chip
                    label="Current Plan"
                    color="primary"
                    sx={{ position: 'absolute', top: 16, right: 16 }}
                  />
                )}
                {tier.type === 'paid' && (
                  <Chip
                    icon={<Star />}
                    label="Popular"
                    color="warning"
                    sx={{ position: 'absolute', top: 16, left: 16 }}
                  />
                )}
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="h5" component="h2" gutterBottom>
                    {tier.name}
                  </Typography>
                  <Box sx={{ my: 2 }}>
                    <Typography variant="h3" component="span" color="primary">
                      ${parseFloat(tier.price).toFixed(2)}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" component="span">
                      /{tier.duration_days === 30 ? 'month' : `${tier.duration_days} days`}
                    </Typography>
                  </Box>
                  <Divider sx={{ my: 2 }} />
                  <Box>
                    <Typography variant="body2" gutterBottom sx={{ fontWeight: 'bold' }}>
                      Features:
                    </Typography>
                    <Box sx={{ mt: 1 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <Check sx={{ color: 'success.main', mr: 1, fontSize: 20 }} />
                        <Typography variant="body2">
                          {features.ads === false ? 'Ad-free experience' : 'Ads included'}
                        </Typography>
                      </Box>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <Check sx={{ color: 'success.main', mr: 1, fontSize: 20 }} />
                        <Typography variant="body2">
                          {features.exclusive_articles ? 'Exclusive articles' : 'Limited articles'}
                        </Typography>
                      </Box>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <Check sx={{ color: 'success.main', mr: 1, fontSize: 20 }} />
                        <Typography variant="body2">
                          {features.offline_reading ? 'Offline reading' : 'Online only'}
                        </Typography>
                      </Box>
                      {features.multiple_users && (
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                          <Check sx={{ color: 'success.main', mr: 1, fontSize: 20 }} />
                          <Typography variant="body2">
                            Multiple users
                          </Typography>
                        </Box>
                      )}
                      {tier.type === 'student' && (
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                          <Check sx={{ color: 'success.main', mr: 1, fontSize: 20 }} />
                          <Typography variant="body2">
                            50% student discount
                          </Typography>
                        </Box>
                      )}
                    </Box>
                  </Box>
                </CardContent>
                <CardActions sx={{ p: 2, pt: 0 }}>
                  <Button
                    fullWidth
                    variant={isCurrentTier ? 'outlined' : 'contained'}
                    color={tier.type === 'paid' ? 'primary' : 'secondary'}
                    onClick={() => handleSubscribe(tier.id, tier.name)}
                    disabled={isCurrentTier || subscribing === tier.id}
                    sx={{ py: 1.5 }}
                  >
                    {subscribing === tier.id ? (
                      <>
                        <CircularProgress size={20} sx={{ mr: 1 }} />
                        Processing...
                      </>
                    ) : isCurrentTier ? (
                      'Current Plan'
                    ) : (
                      'Subscribe Now'
                    )}
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          )
        })}
      </Grid>

      {tiers.length === 0 && (
        <Paper sx={{ p: 4, textAlign: 'center', mt: 3 }}>
          <Typography variant="h6" color="text.secondary">
            No subscription plans available at the moment.
          </Typography>
        </Paper>
      )}

      <Paper sx={{ p: 3, mt: 4, bgcolor: 'grey.50' }}>
        <Typography variant="h6" gutterBottom>
          Why Subscribe?
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle2" gutterBottom>
              📰 Exclusive Content
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Access premium articles and in-depth analysis from our expert journalists
            </Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle2" gutterBottom>
              🚫 Ad-Free Experience
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Enjoy reading without interruptions from advertisements
            </Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle2" gutterBottom>
              📱 Offline Reading
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Download articles and read them anytime, anywhere, even offline
            </Typography>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  )
}

export default Subscription

