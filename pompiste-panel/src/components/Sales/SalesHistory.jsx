import { useSelector } from 'react-redux';
import dayjs from 'dayjs';

const PAYMENT_BADGE = {
  CASH: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
  CREDIT: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400',
};

export default function SalesHistory() {
  const sales = useSelector((s) => s.sales.sales);
  const offlineQueue = useSelector((s) => s.sales.offlineQueue);

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div className="px-5 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
        <h2 className="font-semibold text-gray-900 dark:text-white">Sales History</h2>
        {offlineQueue.length > 0 && (
          <span className="flex items-center gap-1.5 text-xs text-orange-600 dark:text-orange-400 bg-orange-50 dark:bg-orange-900/20 px-3 py-1 rounded-full border border-orange-200 dark:border-orange-700">
            <span className="w-2 h-2 bg-orange-500 rounded-full animate-pulse" />
            {offlineQueue.length} queued offline
          </span>
        )}
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 dark:bg-gray-700/50">
            <tr>
              {['#', 'Time', 'Fuel', 'Qty (L)', 'Amount (RWF)', 'Payment', 'Customer'].map((h) => (
                <th key={h} className="px-4 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
            {offlineQueue.map((s, i) => (
              <tr key={`offline-${i}`} className="bg-orange-50 dark:bg-orange-900/10">
                <td className="px-4 py-3 text-orange-500 font-medium">⏳</td>
                <td className="px-4 py-3 text-gray-400 dark:text-gray-500">Offline</td>
                <td className="px-4 py-3 text-gray-600 dark:text-gray-300">{s.fuel_type}</td>
                <td className="px-4 py-3 text-gray-600 dark:text-gray-300">{Number(s.quantity_liters).toFixed(2)}</td>
                <td className="px-4 py-3 font-medium text-gray-800 dark:text-gray-200">{Number(s.amount).toLocaleString()}</td>
                <td className="px-4 py-3">
                  <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400">
                    {s.payment_type}
                  </span>
                </td>
                <td className="px-4 py-3 text-gray-400">—</td>
              </tr>
            ))}
            {sales.length === 0 && offlineQueue.length === 0 ? (
              <tr>
                <td colSpan={7} className="px-4 py-8 text-center text-gray-400 dark:text-gray-500">
                  No sales yet in this shift
                </td>
              </tr>
            ) : (
              sales.map((s, i) => (
                <tr key={s.id || i} className="hover:bg-gray-50 dark:hover:bg-gray-700/30">
                  <td className="px-4 py-3 text-gray-500 dark:text-gray-400">{i + 1}</td>
                  <td className="px-4 py-3 text-gray-600 dark:text-gray-300">
                    {s.created_at ? dayjs(s.created_at).format('HH:mm') : '—'}
                  </td>
                  <td className="px-4 py-3 font-medium text-gray-900 dark:text-white">{s.fuel_type}</td>
                  <td className="px-4 py-3 text-gray-600 dark:text-gray-300">{Number(s.quantity_liters).toFixed(2)}</td>
                  <td className="px-4 py-3 font-semibold text-gray-800 dark:text-gray-200">
                    {Number(s.amount).toLocaleString()}
                  </td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${PAYMENT_BADGE[s.payment_type] || ''}`}>
                      {s.payment_type}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-600 dark:text-gray-300">
                    {s.customer_name || s.customer || '—'}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
