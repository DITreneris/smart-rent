export interface UserProfile {
  id: string;
  email: string;
  name: string;
  role: 'tenant' | 'landlord' | 'admin';
  wallet_address?: string;
  profile_image?: string;
  phone?: string;
  createdAt: string;
  updatedAt: string;
}

export interface AuthState {
  isAuthenticated: boolean;
  user: UserProfile | null;
  token: string | null;
  loading: boolean;
  error: string | null;
} 