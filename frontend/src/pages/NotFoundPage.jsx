import React from 'react';
import { Link } from 'react-router-dom';

export default function NotFoundPage() {
  return (
    <div className="page centered" style={{ textAlign: 'center' }}>
      <div style={{ fontSize: '4rem', marginBottom: '10px' }}>🔍</div>
      <h1 style={{ color: '#1E293B', marginBottom: '15px' }}>404 — Page Not Found</h1>
      <p style={{ color: '#64748B', marginBottom: '25px' }}>
        We couldn't find the page you were looking for.
      </p>
      <Link to="/" className="btn-primary" style={{ textDecoration: 'none' }}>
        Back to Checkout
      </Link>
    </div>
  );
}
