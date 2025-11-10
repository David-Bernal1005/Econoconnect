import React, { useState, useEffect, useCallback } from 'react';

// Sencillo contenedor de toasts. Se expone window.showToast(msg, type)
// type: 'info' | 'success' | 'error'
export default function ToastContainer() {
  const [toasts, setToasts] = useState([]);

  const removeToast = useCallback((id) => {
    setToasts((prev) => prev.filter(t => t.id !== id));
  }, []);

  useEffect(() => {
    window.showToast = (message, type = 'info') => {
      const id = `${Date.now()}-${Math.random().toString(16).slice(2)}`;
      const toast = { id, message, type };
      setToasts((prev) => [...prev, toast]);
      // Auto eliminar después de 4s
      setTimeout(() => removeToast(id), 4000);
    };
    return () => {
      if (window.showToast) delete window.showToast;
    };
  }, [removeToast]);

  if (!toasts.length) return null;

  return (
    <div style={containerStyle} aria-live="polite" aria-atomic="true">
      {toasts.map(t => (
        <div
          key={t.id}
          style={{ ...toastStyle, ...typeStyles[t.type] }}
          onClick={() => removeToast(t.id)}
          role="alert"
        >
          {t.message}
        </div>
      ))}
    </div>
  );
}

const containerStyle = {
  position: 'fixed',
  top: 16,
  right: 16,
  zIndex: 2000,
  display: 'flex',
  flexDirection: 'column',
  gap: '8px',
  maxWidth: '320px'
};

const toastStyle = {
  padding: '10px 14px',
  borderRadius: '6px',
  fontSize: '14px',
  boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
  cursor: 'pointer',
  lineHeight: 1.3,
  fontWeight: 500,
  background: '#222',
  color: '#fff',
  border: '1px solid #444',
};

const typeStyles = {
  info: {},
  success: { background: '#0d6228', borderColor: '#0d6228' },
  error: { background: '#7d1010', borderColor: '#aa3c3c' }
};
