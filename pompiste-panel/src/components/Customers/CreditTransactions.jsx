import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { createCreditTransaction } from '../../services/customerService';
import CustomerLookup from './CustomerLookup';
import dayjs from 'dayjs';

export default function CreditTransactions({ addToast }) {
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm();

  const onSubmit = async (data) => {
    if (!selectedCustomer) { addToast('Select a customer first', 'warning'); return; }
    try {
      const res = await createCreditTransaction({
        customer: selectedCustomer.id,
        amount: parseFloat(data.amount),
        type: data.type,
        note: data.note,
      });
      setTransactions((prev) => [res.data, ...prev]);
      addToast('Transaction recorded', 'success');
      reset();
    } catch (err) {
      const msg = err.response?.data?.detail || 'Transaction failed';
      addToast(String(msg), 'error');
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6 max-w-lg">
        <h2 className="font-bold text-gray-900 dark:text-white mb-4">Credit Transaction</h2>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Customer</label>
          <CustomerLookup selected={selectedCustomer} onSelect={setSelectedCustomer} />
        </div>

        {selectedCustomer && (
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Type</label>
                <select
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  {...register('type', { required: 'Required' })}
                >
                  <option value="DEBIT">Debit (charge)</option>
                  <option value="CREDIT">Credit (payment)</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Amount (RWF)</label>
                <input
                  type="number"
                  min="1"
                  step="any"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  {...register('amount', { required: 'Required', min: { value: 1, message: '> 0' } })}
                />
                {errors.amount && <p className="mt-1 text-xs text-red-500">{errors.amount.message}</p>}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Note (optional)</label>
              <input
                type="text"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                {...register('note')}
              />
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white font-semibold rounded-lg transition-colors"
            >
              {isSubmitting ? 'Saving…' : 'Record Transaction'}
            </button>
          </form>
        )}
      </div>

      {transactions.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
          <div className="px-5 py-4 border-b border-gray-200 dark:border-gray-700">
            <h3 className="font-semibold text-gray-900 dark:text-white">Recent Transactions</h3>
          </div>
          <table className="w-full text-sm">
            <thead className="bg-gray-50 dark:bg-gray-700/50">
              <tr>
                {['Time', 'Customer', 'Type', 'Amount'].map((h) => (
                  <th key={h} className="px-4 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
              {transactions.map((t, i) => (
                <tr key={t.id || i}>
                  <td className="px-4 py-3 text-gray-500">{t.created_at ? dayjs(t.created_at).format('HH:mm') : 'Just now'}</td>
                  <td className="px-4 py-3 font-medium text-gray-900 dark:text-white">{selectedCustomer?.name}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${t.type === 'CREDIT' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'}`}>
                      {t.type}
                    </span>
                  </td>
                  <td className="px-4 py-3 font-semibold text-gray-800 dark:text-gray-200">{Number(t.amount).toLocaleString()} RWF</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
