import { useState } from 'react';
import api from '../../services/api';
import dayjs from 'dayjs';
import ReportExporter from './ReportExporter';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

export default function DailySalesReport({ addToast }) {
  const [date, setDate] = useState(dayjs().format('YYYY-MM-DD'));
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchReport = async () => {
    setLoading(true);
    try {
      const res = await api.get('/reports/daily/', { params: { date } });
      setReport(res.data);
    } catch {
      addToast?.('Failed to load report', 'error');
      setReport(null);
    } finally {
      setLoading(false);
    }
  };

  const fuelBreakdown = report
    ? Object.entries(report.fuel_breakdown || {}).map(([ft, data]) => ({
        fuel_type: ft,
        liters: parseFloat(data.liters || 0),
        amount: parseFloat(data.amount || 0),
      }))
    : [];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row gap-3 items-start sm:items-end">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Date</label>
          <input
            type="date"
            value={date}
            max={dayjs().format('YYYY-MM-DD')}
            onChange={(e) => setDate(e.target.value)}
            className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button
          onClick={fetchReport}
          disabled={loading}
          className="px-5 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white font-semibold rounded-lg transition-colors"
        >
          {loading ? 'Loading…' : 'Load Report'}
        </button>
        {report && <ReportExporter report={report} date={date} />}
      </div>

      {report && (
        <>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { label: 'Total Sales', value: `${Number(report.total_amount || 0).toLocaleString()} RWF`, color: 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300' },
              { label: 'Total Liters', value: `${Number(report.total_liters || 0).toFixed(1)} L`, color: 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300' },
              { label: 'Cash', value: `${Number(report.cash_amount || 0).toLocaleString()} RWF`, color: 'bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-300' },
              { label: 'Credit', value: `${Number(report.credit_amount || 0).toLocaleString()} RWF`, color: 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-300' },
            ].map(({ label, value, color }) => (
              <div key={label} className={`rounded-xl p-5 ${color}`}>
                <p className="text-xs font-semibold uppercase tracking-wide opacity-70">{label}</p>
                <p className="text-xl font-bold mt-1">{value}</p>
              </div>
            ))}
          </div>

          {fuelBreakdown.length > 0 && (
            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5">
              <h3 className="font-semibold text-gray-700 dark:text-gray-300 mb-4">Fuel Breakdown</h3>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={fuelBreakdown}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="fuel_type" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip formatter={(v, n) => n === 'liters' ? [`${v.toFixed(2)} L`, 'Liters'] : [`${Number(v).toLocaleString()} RWF`, 'Amount']} />
                  <Bar dataKey="liters" name="liters" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="amount" name="amount" fill="#10b981" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>

              <table className="w-full text-sm mt-4">
                <thead className="bg-gray-50 dark:bg-gray-700/50">
                  <tr>
                    {['Fuel Type', 'Liters', 'Amount (RWF)', 'Transactions'].map((h) => (
                      <th key={h} className="px-4 py-2 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                  {fuelBreakdown.map((row) => (
                    <tr key={row.fuel_type}>
                      <td className="px-4 py-2 font-medium text-gray-900 dark:text-white">{row.fuel_type}</td>
                      <td className="px-4 py-2 text-gray-600 dark:text-gray-300">{row.liters.toFixed(2)}</td>
                      <td className="px-4 py-2 text-gray-600 dark:text-gray-300">{row.amount.toLocaleString()}</td>
                      <td className="px-4 py-2 text-gray-600 dark:text-gray-300">
                        {report.fuel_breakdown?.[row.fuel_type]?.count ?? '—'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  );
}
