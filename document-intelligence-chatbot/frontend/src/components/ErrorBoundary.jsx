import React from 'react';

/**
 * ErrorBoundary — catches any unhandled React render errors and shows a
 * friendly fallback UI instead of a blank white screen.
 */
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, info) {
        console.error('ErrorBoundary caught an error:', error, info);
    }

    handleReset = () => {
        this.setState({ hasError: false, error: null });
    };

    render() {
        if (this.state.hasError) {
            return (
                <div className="error-boundary">
                    <div className="error-boundary-card">
                        <div className="error-icon">⚠️</div>
                        <h2>Something went wrong</h2>
                        <p>The app encountered an unexpected error. You can try reloading the page.</p>
                        {this.state.error && (
                            <pre className="error-details">{this.state.error.message}</pre>
                        )}
                        <div className="error-actions">
                            <button className="btn btn-primary" onClick={() => window.location.reload()}>
                                Reload Page
                            </button>
                            <button className="btn btn-secondary" onClick={this.handleReset}>
                                Try Again
                            </button>
                        </div>
                    </div>
                </div>
            );
        }
        return this.props.children;
    }
}

export default ErrorBoundary;
