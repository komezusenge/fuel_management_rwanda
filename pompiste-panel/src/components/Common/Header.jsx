import { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import dayjs from 'dayjs';
import LogoutButton from '../Auth/LogoutButton';

export default function Header({ onToggleDark, isDark }) {
  const user = useSelector((s) => s.auth.user);
  const [time, setTime] = useState(dayjs().format('HH:mm:ss'));

  useEffect(() => {
    const id = setInterval(() => setTime(dayjs().format('HH:mm:ss')), 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <header className="bg-blue-700 dark:bg-gray-900 text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-blue-500 dark:bg-blue-700 rounded-full flex items-center justify-center font-bold text-sm">
            FMS
          </div>
          <div>
            <span className="font-semibold text-sm">Fuel Management</span>
            <span className="hidden sm:inline text-blue-200 dark:text-gray-400 text-xs ml-2">Pompiste Panel</span>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <span className="font-mono text-sm text-blue-100 dark:text-gray-300 hidden md:block">{time}</span>

          {user && (
            <span className="text-sm text-blue-100 dark:text-gray-300 hidden sm:block">
              {user.first_name || user.username || user.email}
            </span>
          )}

          <button
            onClick={onToggleDark}
            className="p-2 rounded-lg bg-blue-600 dark:bg-gray-700 hover:bg-blue-500 dark:hover:bg-gray-600 transition-colors"
            title="Toggle dark mode"
          >
            {isDark ? (
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707M17.657 17.657l-.707-.707M6.343 6.343l-.707-.707M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            ) : (
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
              </svg>
            )}
          </button>

          <LogoutButton />
        </div>
      </div>
    </header>
  );
}
