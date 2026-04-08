import { useForm } from 'react-hook-form';
import { closeShift } from '../../services/shiftService';
import { useState } from 'react';

export default function CloseShiftModal({ shift, sales, onClose, onSuccess }) {
  const [error, setError] = useState('');
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm();

  const totalLiters = sales.reduce((a, s) => a + parseFloat(s.quantity_liters || 0), 0);
  const totalCash = sales.filter((s) => s.payment_type === 'CASH').reduce((a, s) => a + parseFloat(s.amount || 0), 0);
  const totalCredit = sales.filter((s) => s.payment_type === 'CREDIT').reduce((a, s) => a + parseFloat(s.amount || 0), 0);

  const onSubmit = async (data) => {
    setError('');
    try {
      await closeShift(shift.id, {
        ending_cash: parseFloat(data.ending_cash),
        closing_meter: parseFloat(data.closing_meter),
      });
      onSuccess();
    } catch (err) {
      const msg = err.response?.data?.detail
        || Object.values(err.response?.data || {}).flat()[0]
        || 'Failed to close shift';
      setError(String(msg));
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-full max-w-md p-6">
        <div className="flex items-center justify-between mb-5">
          <h2 className="text-lg font-bold text-gray-900 dark:text-white">Close Shift</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Summary */}
        <div className="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4 mb-5 grid grid-cols-2 gap-3 text-sm">
          <div>
            <p className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">Total Liters</p>
            <p className="font-semibold text-gray-800 dark:text-gray-200">{totalLiters.toFixed(2)} L</p>
          </div>
          <div>
            <p className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">Transactions</p>
            <p className="font-semibold text-gray-800 dark:text-gray-200">{sales.length}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">Cash</p>
            <p className="font-semibold text-green-600 dark:text-green-400">{totalCash.toLocaleString()} RWF</p>
          </div>
          <div>
            <p className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">Credit</p>
            <p className="font-semibold text-yellow-600 dark:text-yellow-400">{totalCredit.toLocaleString()} RWF</p>
          </div>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-700 text-red-700 dark:text-red-300 rounded-lg text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Ending Cash (RWF)</label>
            <input
              type="number"
              min="0"
              step="any"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              {...register('ending_cash', { required: 'Required', min: { value: 0, message: 'Must be ≥ 0' } })}
            />
            {errors.ending_cash && <p className="mt-1 text-xs text-red-500">{errors.ending_cash.message}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Closing Meter (L)</label>
            <input
              type="number"
              min="0"
              step="any"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              {...register('closing_meter', { required: 'Required', min: { value: 0, message: 'Must be ≥ 0' } })}
            />
            {errors.closing_meter && <p className="mt-1 text-xs text-red-500">{errors.closing_meter.message}</p>}
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 py-2.5 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex-1 py-2.5 bg-red-600 hover:bg-red-700 disabled:opacity-60 text-white rounded-lg transition-colors text-sm font-semibold"
            >
              {isSubmitting ? 'Closing…' : 'Close Shift'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
