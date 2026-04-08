import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { useSelector, useDispatch } from 'react-redux';
import { createSale, getFuelPrices } from '../../services/salesService';
import { getCustomers } from '../../services/customerService';
import { addSale, setPrices, enqueueOfflineSale } from '../../store/salesSlice';
import ReceiptPrinter from './ReceiptPrinter';

const FUEL_TYPES = ['PETROL', 'DIESEL', 'SUPER'];
const PAYMENT_TYPES = ['CASH', 'CREDIT'];

export default function SalesEntry({ addToast }) {
  const dispatch = useDispatch();
  const currentShift = useSelector((s) => s.shift.currentShift);
  const prices = useSelector((s) => s.sales.prices);
  const [customers, setCustomers] = useState([]);
  const [receipt, setReceipt] = useState(null);
  const [calcMode, setCalcMode] = useState('liters'); // 'liters' | 'amount'

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    reset,
    formState: { errors, isSubmitting },
  } = useForm({ defaultValues: { fuel_type: 'PETROL', payment_type: 'CASH' } });

  const watchFuelType = watch('fuel_type');
  const watchQuantity = watch('quantity_liters');
  const watchAmount = watch('amount');
  const watchPayment = watch('payment_type');

  useEffect(() => {
    getFuelPrices()
      .then((res) => {
        const p = {};
        (Array.isArray(res.data) ? res.data : res.data.results || []).forEach((item) => {
          p[item.fuel_type] = parseFloat(item.price_per_liter);
        });
        dispatch(setPrices(p));
      })
      .catch(() => {});

    getCustomers()
      .then((res) => setCustomers(Array.isArray(res.data) ? res.data : res.data.results || []))
      .catch(() => {});
  }, []);

  // Auto-calculate amount from liters
  useEffect(() => {
    if (calcMode === 'liters' && watchQuantity && prices[watchFuelType]) {
      setValue('amount', (parseFloat(watchQuantity) * prices[watchFuelType]).toFixed(0), { shouldValidate: false });
    }
  }, [watchQuantity, watchFuelType, calcMode, prices, setValue]);

  // Auto-calculate liters from amount
  useEffect(() => {
    if (calcMode === 'amount' && watchAmount && prices[watchFuelType]) {
      setValue('quantity_liters', (parseFloat(watchAmount) / prices[watchFuelType]).toFixed(2), { shouldValidate: false });
    }
  }, [watchAmount, watchFuelType, calcMode, prices, setValue]);

  if (!currentShift) {
    return (
      <div className="text-center py-12 text-gray-500 dark:text-gray-400">
        <p className="text-lg font-medium">No active shift</p>
        <p className="text-sm mt-1">Please open a shift from the Dashboard first.</p>
      </div>
    );
  }

  const onSubmit = async (data) => {
    const payload = {
      shift: currentShift.id,
      fuel_type: data.fuel_type,
      quantity_liters: parseFloat(data.quantity_liters),
      amount: parseFloat(data.amount),
      payment_type: data.payment_type,
      ...(data.payment_type === 'CREDIT' && data.customer ? { customer: Number(data.customer) } : {}),
    };

    try {
      const res = await createSale(payload);
      dispatch(addSale(res.data));
      setReceipt(res.data);
      reset({ fuel_type: 'PETROL', payment_type: 'CASH' });
      addToast('Sale recorded successfully', 'success');
    } catch (err) {
      if (!navigator.onLine || err.code === 'ERR_NETWORK') {
        dispatch(enqueueOfflineSale({ ...payload, _offline: true, _id: Date.now() }));
        addToast('Offline: sale queued for sync', 'warning');
        reset({ fuel_type: 'PETROL', payment_type: 'CASH' });
      } else {
        const msg = err.response?.data?.detail
          || Object.values(err.response?.data || {}).flat()[0]
          || 'Failed to record sale';
        addToast(String(msg), 'error');
      }
    }
  };

  const pricePerLiter = prices[watchFuelType] ? `${Number(prices[watchFuelType]).toLocaleString()} RWF/L` : 'Price N/A';

  return (
    <>
      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6 max-w-lg">
        <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-1">New Sale</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mb-5">
          Shift #{currentShift.id} · Pump {currentShift.pump} · {pricePerLiter}
        </p>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Fuel Type</label>
              <select
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                {...register('fuel_type', { required: 'Required' })}
              >
                {FUEL_TYPES.map((f) => <option key={f} value={f}>{f}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Payment</label>
              <select
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                {...register('payment_type', { required: 'Required' })}
              >
                {PAYMENT_TYPES.map((p) => <option key={p} value={p}>{p}</option>)}
              </select>
            </div>
          </div>

          {/* Calc mode toggle */}
          <div className="flex rounded-lg border border-gray-300 dark:border-gray-600 overflow-hidden text-sm">
            <button
              type="button"
              onClick={() => setCalcMode('liters')}
              className={`flex-1 py-2 font-medium transition-colors ${calcMode === 'liters' ? 'bg-blue-600 text-white' : 'bg-white dark:bg-gray-700 text-gray-600 dark:text-gray-300'}`}
            >
              Enter Liters
            </button>
            <button
              type="button"
              onClick={() => setCalcMode('amount')}
              className={`flex-1 py-2 font-medium transition-colors ${calcMode === 'amount' ? 'bg-blue-600 text-white' : 'bg-white dark:bg-gray-700 text-gray-600 dark:text-gray-300'}`}
            >
              Enter Amount
            </button>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Quantity (L) {calcMode === 'amount' && <span className="text-xs text-gray-400">(auto)</span>}
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                readOnly={calcMode === 'amount'}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 read-only:bg-gray-50 dark:read-only:bg-gray-700/50"
                {...register('quantity_liters', {
                  required: 'Required',
                  min: { value: 0.01, message: 'Must be > 0' },
                })}
              />
              {errors.quantity_liters && <p className="mt-1 text-xs text-red-500">{errors.quantity_liters.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Amount (RWF) {calcMode === 'liters' && <span className="text-xs text-gray-400">(auto)</span>}
              </label>
              <input
                type="number"
                step="1"
                min="0"
                readOnly={calcMode === 'liters'}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 read-only:bg-gray-50 dark:read-only:bg-gray-700/50"
                {...register('amount', {
                  required: 'Required',
                  min: { value: 1, message: 'Must be > 0' },
                })}
              />
              {errors.amount && <p className="mt-1 text-xs text-red-500">{errors.amount.message}</p>}
            </div>
          </div>

          {watchPayment === 'CREDIT' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Customer</label>
              <select
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                {...register('customer', { required: watchPayment === 'CREDIT' ? 'Required for credit' : false })}
              >
                <option value="">Select customer…</option>
                {customers.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name} {c.phone ? `(${c.phone})` : ''}
                  </option>
                ))}
              </select>
              {errors.customer && <p className="mt-1 text-xs text-red-500">{errors.customer.message}</p>}
            </div>
          )}

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white font-semibold rounded-lg transition-colors"
          >
            {isSubmitting ? 'Saving…' : 'Record Sale'}
          </button>
        </form>
      </div>

      {receipt && (
        <ReceiptPrinter sale={receipt} onClose={() => setReceipt(null)} />
      )}
    </>
  );
}
