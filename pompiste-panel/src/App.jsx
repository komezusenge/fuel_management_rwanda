import { useState, useCallback } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import Header from './components/Common/Header';
import Navigation from './components/Common/Navigation';
import NotificationToast from './components/Common/NotificationToast';
import LoginPage from './components/Auth/LoginPage';
import DashboardPage from './pages/DashboardPage';
import SalesPage from './pages/SalesPage';
import ReportsPage from './pages/ReportsPage';
import ProfilePage from './pages/ProfilePage';

function ProtectedLayout({ children, isDark, onToggleDark }) {
  const isAuthenticated = useSelector((s) => s.auth.isAuthenticated);
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return (
    <div className="min-h-screen flex flex-col">
      <Header isDark={isDark} onToggleDark={onToggleDark} />
      <Navigation />
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-6">
        {children}
      </main>
    </div>
  );
}

export default function App() {
  const [toasts, setToasts] = useState([]);
  const [isDark, setIsDark] = useState(() => {
    const saved = localStorage.getItem('theme');
    if (saved) return saved === 'dark';
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  const addToast = useCallback((message, type = 'info', duration = 4000) => {
    const id = Date.now() + Math.random();
    setToasts((prev) => [...prev, { id, message, type, duration }]);
  }, []);

  const removeToast = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const toggleDark = () => {
    setIsDark((prev) => {
      const next = !prev;
      localStorage.setItem('theme', next ? 'dark' : 'light');
      return next;
    });
  };

  return (
    <div className={isDark ? 'dark' : ''}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/"
            element={
              <ProtectedLayout isDark={isDark} onToggleDark={toggleDark}>
                <DashboardPage addToast={addToast} />
              </ProtectedLayout>
            }
          />
          <Route
            path="/sales"
            element={
              <ProtectedLayout isDark={isDark} onToggleDark={toggleDark}>
                <SalesPage addToast={addToast} />
              </ProtectedLayout>
            }
          />
          <Route
            path="/reports"
            element={
              <ProtectedLayout isDark={isDark} onToggleDark={toggleDark}>
                <ReportsPage addToast={addToast} />
              </ProtectedLayout>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedLayout isDark={isDark} onToggleDark={toggleDark}>
                <ProfilePage addToast={addToast} />
              </ProtectedLayout>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
      <NotificationToast toasts={toasts} onRemove={removeToast} />
    </div>
  );
}

