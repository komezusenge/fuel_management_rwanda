import { useForm } from 'react-hook-form';
import { openShift } from '../../services/shiftService';
import { useState } from 'react';

const FUEL_TYPES = ['PETROL', 'DIESEL', 'SUPER'];

export default function OpenShiftModal({ onClose, onSuccess }) {
  const [error, setError] = useState('');
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm();

  const onSubmit = async (data) => {
    setError('');
    try {
      const res = await openShift({
        pump: Number(data.pump),
        tank: data.tank,
        fuel_type: data.fuel_type,
        starting_cash: parseFloat(data.starting_cash),
        opening_meter: parseFloat(data.opening_meter),
      });
      onSuccess(res.data);
    } catch (err) {
      const msg = err.response?.data?.detail
        || Object.values(err.response?.data || {}).flat()[0]
        || 'Failed to open shift';
      setError(String(msg));
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-full max-w-md p-6">
        <div className="flex items-center justify-between mb-5">
          <h2 className="text-lg font-bold text-gray-900 dark:text-white">Open Shift</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-700 text-red-700 dark:text-red-300 rounded-lg text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Pump #</label>
              <input
                type="number"
                min="1"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                {...register('pump', { required: 'Required' })}
              />
              {errors.pump && <p className="mt-1 text-xs text-red-500">{errors.pump.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Tank</label>
              <input
                type="text"
                placeholder="e.g. T1"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                {...register('tank', { required: 'Required' })}
              />
              {errors.tank && <p className="mt-1 text-xs text-red-500">{errors.tank.message}</p>}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Fuel Type</label>
            <select
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              {...register('fuel_type', { required: 'Required' })}
            >
              <option value="">Select fuel type</option>
              {FUEL_TYPES.map((f) => <option key={f} value={f}>{f}</option>)}
            </select>
            {errors.fuel_type && <p className="mt-1 text-xs text-red-500">{errors.fuel_type.message}</p>}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Starting Cash (RWF)</label>
              <input
                type="number"
                min="0"
                step="any"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                {...register('starting_cash', { required: 'Required', min: { value: 0, message: 'Must be ≥ 0' } })}
              />
              {errors.starting_cash && <p className="mt-1 text-xs text-red-500">{errors.starting_cash.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Opening Meter (L)</label>
              <input
                type="number"
                min="0"
                step="any"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                {...register('opening_meter', { required: 'Required', min: { value: 0, message: 'Must be ≥ 0' } })}
              />
              {errors.opening_meter && <p className="mt-1 text-xs text-red-500">{errors.opening_meter.message}</p>}
            </div>
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
              className="flex-1 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white rounded-lg transition-colors text-sm font-semibold"
            >
              {isSubmitting ? 'Opening…' : 'Open Shift'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
