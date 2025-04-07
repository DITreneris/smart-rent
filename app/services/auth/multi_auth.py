"""
Multi-factor authentication service for SmartRent platform.
Handles wallet-based and OAuth authentication.
"""
from typing import Dict, Optional
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class MultiFactorAuth:
    """Handles multiple authentication methods."""
    
    def __init__(self, config: Dict):
        """Initialize authentication service with configuration."""
        self.google_client_id = config['google_client_id']
        self.jwt_secret = config['jwt_secret']
        self.jwt_algorithm = config.get('jwt_algorithm', 'HS256')
        self.token_expiry = config.get('token_expiry', 24)  # hours
        
    async def verify_google_token(self, token: str) -> Dict:
        """Verify Google OAuth token."""
        try:
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                self.google_client_id
            )
            
            return {
                'success': True,
                'user_id': idinfo['sub'],
                'email': idinfo['email'],
                'name': idinfo.get('name')
            }
        except Exception as e:
            logger.error(f"Google token verification failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    async def verify_wallet_signature(
        self, 
        address: str, 
        signature: str, 
        message: str
    ) -> Dict:
        """Verify wallet signature."""
        try:
            # Implement wallet signature verification logic
            # This will vary based on the blockchain platform
            is_valid = True  # Placeholder for actual verification
            
            return {
                'success': is_valid,
                'address': address
            }
        except Exception as e:
            logger.error(f"Wallet signature verification failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    async def create_session(
        self, 
        user_data: Dict, 
        wallet_address: str
    ) -> Dict:
        """Create a session with JWT token."""
        try:
            payload = {
                'user_id': user_data['user_id'],
                'email': user_data['email'],
                'wallet_address': wallet_address,
                'exp': datetime.utcnow() + timedelta(hours=self.token_expiry)
            }
            
            token = jwt.encode(
                payload,
                self.jwt_secret,
                algorithm=self.jwt_algorithm
            )
            
            return {
                'success': True,
                'token': token,
                'expires_in': self.token_expiry * 3600  # seconds
            }
        except Exception as e:
            logger.error(f"Session creation failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    async def verify_session(self, token: str) -> Dict:
        """Verify a session token."""
        try:
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=[self.jwt_algorithm]
            )
            
            return {
                'success': True,
                'user_id': payload['user_id'],
                'email': payload['email'],
                'wallet_address': payload['wallet_address']
            }
        except jwt.ExpiredSignatureError:
            return {
                'success': False,
                'error': 'Token has expired'
            }
        except jwt.InvalidTokenError as e:
            return {
                'success': False,
                'error': f'Invalid token: {str(e)}'
            }
            
    async def authenticate_user(
        self, 
        google_token: str,
        wallet_address: str,
        wallet_signature: str,
        message: str
    ) -> Dict:
        """Complete multi-factor authentication."""
        # Verify Google token
        google_result = await self.verify_google_token(google_token)
        if not google_result['success']:
            return google_result
            
        # Verify wallet signature
        wallet_result = await self.verify_wallet_signature(
            wallet_address,
            wallet_signature,
            message
        )
        if not wallet_result['success']:
            return wallet_result
            
        # Create session if both verifications pass
        return await self.create_session(google_result, wallet_address) 