import SalesEntry from '../components/Sales/SalesEntry';
import SalesHistory from '../components/Sales/SalesHistory';
import { useDispatch, useSelector } from 'react-redux';
import { useEffect } from 'react';
import { setSales } from '../store/salesSlice';
import { getSales } from '../services/salesService';
import { removeOfflineSale } from '../store/salesSlice';
import { createSale } from '../services/salesService';

export default function SalesPage({ addToast }) {
  const dispatch = useDispatch();
  const currentShift = useSelector((s) => s.shift.currentShift);
  const offlineQueue = useSelector((s) => s.sales.offlineQueue);

  // Load sales when shift changes
  useEffect(() => {
    if (!currentShift?.id) return;
    getSales({ shift: currentShift.id })
      .then((res) => dispatch(setSales(Array.isArray(res.data) ? res.data : res.data.results || [])))
      .catch(() => {});
  }, [currentShift?.id]);

  // Sync offline queue when connection is restored
  useEffect(() => {
    const sync = async () => {
      if (offlineQueue.length === 0) return;
      let syncedCount = 0;
      for (let i = offlineQueue.length - 1; i >= 0; i--) {
        const { _offline, _id, ...payload } = offlineQueue[i];
        try {
          await createSale(payload);
          dispatch(removeOfflineSale(i));
          syncedCount++;
        } catch {
          break;
        }
      }
      if (syncedCount > 0) {
        addToast(`${syncedCount} offline sale(s) synced`, 'success');
        if (currentShift?.id) {
          const res = await getSales({ shift: currentShift.id }).catch(() => null);
          if (res) dispatch(setSales(Array.isArray(res.data) ? res.data : res.data.results || []));
        }
      }
    };

    window.addEventListener('online', sync);
    return () => window.removeEventListener('online', sync);
  }, [offlineQueue, currentShift?.id]);

  return (
    <div>
      <h1 className="text-xl font-bold text-gray-900 dark:text-white mb-5">Sales</h1>
      <div className="grid lg:grid-cols-2 gap-6">
        <SalesEntry addToast={addToast} />
        <SalesHistory />
      </div>
    </div>
  );
}
