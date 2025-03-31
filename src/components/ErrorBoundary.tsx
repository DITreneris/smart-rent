import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AppError, ErrorType } from '../utils/ErrorHandler';
import { Button, Alert, Card, Container } from 'react-bootstrap';

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: (error: Error, resetError: () => void) => ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { 
      hasError: false, 
      error: null 
    };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { 
      hasError: true, 
      error 
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    console.error('Error caught by ErrorBoundary:', error, errorInfo);
    
    // Log to error tracking service (like Sentry)
    // if (window.Sentry) {
    //   window.Sentry.captureException(error);
    // }
  }

  resetError = (): void => {
    this.setState({ 
      hasError: false, 
      error: null 
    });
  }

  render(): ReactNode {
    if (this.state.hasError) {
      // Use custom fallback if provided
      if (this.props.fallback) {
        return this.props.fallback(this.state.error!, this.resetError);
      }

      // Default error UI
      const isAppError = this.state.error instanceof AppError;
      const errorType = isAppError ? (this.state.error as AppError).type : ErrorType.UNKNOWN_ERROR;
      
      return (
        <Container className="error-boundary-container">
          <Card className="error-boundary-card">
            <Card.Header className="error-boundary-header">
              <h2>Something went wrong</h2>
            </Card.Header>
            <Card.Body>
              <Alert variant={this.getAlertVariant(errorType)}>
                {this.state.error?.message}
              </Alert>
              
              {this.getErrorGuidance(errorType)}
              
              <div className="error-actions">
                <Button 
                  variant="primary" 
                  onClick={this.resetError}
                  className="retry-button"
                >
                  Try Again
                </Button>
                
                <Button 
                  variant="outline-secondary" 
                  onClick={() => window.location.href = '/'}
                  className="home-button"
                >
                  Go to Home
                </Button>
              </div>
            </Card.Body>
          </Card>
        </Container>
      );
    }

    return this.props.children;
  }
  
  private getAlertVariant(errorType: ErrorType): string {
    switch (errorType) {
      case ErrorType.AUTH_ERROR:
      case ErrorType.SESSION_EXPIRED:
      case ErrorType.PERMISSION_DENIED:
        return 'warning';
        
      case ErrorType.NETWORK_ERROR:
      case ErrorType.SERVER_ERROR:
      case ErrorType.API_ERROR:
        return 'danger';
        
      case ErrorType.WEB3_CONNECTION_ERROR:
      case ErrorType.WEB3_TRANSACTION_ERROR:
      case ErrorType.WALLET_ERROR:
      case ErrorType.CONTRACT_ERROR:
        return 'info';
        
      case ErrorType.VALIDATION_ERROR:
      case ErrorType.FORM_ERROR:
        return 'warning';
        
      default:
        return 'danger';
    }
  }
  
  private getErrorGuidance(errorType: ErrorType): ReactNode {
    switch (errorType) {
      case ErrorType.AUTH_ERROR:
      case ErrorType.SESSION_EXPIRED:
        return (
          <div className="error-guidance">
            <p>Your session may have expired. Please try logging in again.</p>
            <Button 
              variant="link" 
              onClick={() => window.location.href = '/login'}
            >
              Go to Login
            </Button>
          </div>
        );
        
      case ErrorType.PERMISSION_DENIED:
        return (
          <div className="error-guidance">
            <p>You don't have permission to access this resource.</p>
          </div>
        );
        
      case ErrorType.NETWORK_ERROR:
        return (
          <div className="error-guidance">
            <p>Please check your internet connection and try again.</p>
          </div>
        );
        
      case ErrorType.SERVER_ERROR:
        return (
          <div className="error-guidance">
            <p>Our servers are experiencing issues. Please try again later.</p>
          </div>
        );
        
      case ErrorType.WEB3_CONNECTION_ERROR:
      case ErrorType.WALLET_ERROR:
        return (
          <div className="error-guidance">
            <p>There was a problem connecting to your wallet:</p>
            <ul>
              <li>Make sure your wallet is unlocked</li>
              <li>Check that you're connected to the correct network</li>
              <li>Try refreshing the page</li>
            </ul>
          </div>
        );
        
      case ErrorType.WEB3_TRANSACTION_ERROR:
      case ErrorType.CONTRACT_ERROR:
        return (
          <div className="error-guidance">
            <p>Your blockchain transaction couldn't be processed:</p>
            <ul>
              <li>Check that you have sufficient funds</li>
              <li>Make sure you're on the correct network</li>
              <li>Try with a higher gas price</li>
            </ul>
          </div>
        );
        
      default:
        return (
          <div className="error-guidance">
            <p>An unexpected error occurred. Please try again or contact support if the issue persists.</p>
          </div>
        );
    }
  }
}

export default ErrorBoundary; 