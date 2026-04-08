import { useSelector } from 'react-redux';
import CreditTransactions from '../components/Customers/CreditTransactions';

export default function ProfilePage({ addToast }) {
  const user = useSelector((s) => s.auth.user);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-xl font-bold text-gray-900 dark:text-white mb-5">Profile</h1>
        {user && (
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6 max-w-sm">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center text-xl font-bold text-blue-600 dark:text-blue-300">
                {(user.first_name?.[0] || user.username?.[0] || user.email?.[0] || '?').toUpperCase()}
              </div>
              <div>
                <p className="font-semibold text-gray-900 dark:text-white">
                  {user.first_name && user.last_name
                    ? `${user.first_name} ${user.last_name}`
                    : user.username || user.email}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">{user.email}</p>
                {user.role && (
                  <span className="mt-1 inline-block px-2 py-0.5 text-xs font-medium bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-full">
                    {user.role}
                  </span>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      <div>
        <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-4">Customer Credit</h2>
        <CreditTransactions addToast={addToast} />
      </div>
    </div>
  );
}
