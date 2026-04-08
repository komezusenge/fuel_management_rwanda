import { useDispatch } from 'react-redux';
import { logout as logoutAction } from '../../store/authSlice';
import { logout as logoutApi } from '../../services/authService';

export default function LogoutButton({ className = '' }) {
  const dispatch = useDispatch();

  const handleLogout = async () => {
    try {
      await logoutApi();
    } catch {
      // ignore API errors during logout
    } finally {
      dispatch(logoutAction());
    }
  };

  return (
    <button
      onClick={handleLogout}
      className={`flex items-center gap-2 text-sm font-medium text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 transition-colors ${className}`}
    >
      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
      </svg>
      Sign out
    </button>
  );
}
