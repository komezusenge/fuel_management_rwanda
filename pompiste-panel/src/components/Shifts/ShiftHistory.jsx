import { useEffect, useState } from 'react';
import { getShifts } from '../../services/shiftService';
import dayjs from 'dayjs';

const STATUS_BADGE = {
  OPEN: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
  CLOSED: 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400',
};

export default function ShiftHistory({ addToast }) {
  const [shifts, setShifts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await getShifts();
        setShifts(Array.isArray(res.data) ? res.data : res.data.results || []);
      } catch {
        addToast?.('Failed to load shift history', 'error');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center py-8">
        <div className="animate-spin w-6 h-6 border-4 border-blue-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div className="px-5 py-4 border-b border-gray-200 dark:border-gray-700">
        <h2 className="font-semibold text-gray-900 dark:text-white">Shift History</h2>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 dark:bg-gray-700/50">
            <tr>
              {['Pump', 'Fuel', 'Status', 'Opened', 'Closed', 'Opening Meter', 'Closing Meter'].map((h) => (
                <th key={h} className="px-4 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
            {shifts.length === 0 ? (
              <tr>
                <td colSpan={7} className="px-4 py-8 text-center text-gray-400 dark:text-gray-500">
                  No shifts found
                </td>
              </tr>
            ) : (
              shifts.map((shift) => (
                <tr key={shift.id} className="hover:bg-gray-50 dark:hover:bg-gray-700/30">
                  <td className="px-4 py-3 font-medium text-gray-900 dark:text-white">{shift.pump}</td>
                  <td className="px-4 py-3 text-gray-600 dark:text-gray-300">{shift.fuel_type}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${STATUS_BADGE[shift.status] || STATUS_BADGE.CLOSED}`}>
                      {shift.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-600 dark:text-gray-300">
                    {dayjs(shift.created_at).format('DD/MM/YY HH:mm')}
                  </td>
                  <td className="px-4 py-3 text-gray-600 dark:text-gray-300">
                    {shift.closed_at ? dayjs(shift.closed_at).format('DD/MM/YY HH:mm') : '—'}
                  </td>
                  <td className="px-4 py-3 text-gray-600 dark:text-gray-300">
                    {Number(shift.opening_meter).toLocaleString()}
                  </td>
                  <td className="px-4 py-3 text-gray-600 dark:text-gray-300">
                    {shift.closing_meter ? Number(shift.closing_meter).toLocaleString() : '—'}
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
