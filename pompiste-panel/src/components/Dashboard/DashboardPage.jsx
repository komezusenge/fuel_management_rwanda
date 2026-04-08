import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { setCurrentShift } from '../../store/shiftSlice';
import { setSales } from '../../store/salesSlice';
import { getCurrentShift } from '../../services/shiftService';
import { getSales } from '../../services/salesService';
import ShiftInfo from './ShiftInfo';
import SalesChart from './SalesChart';
import OpenShiftModal from '../Shifts/OpenShiftModal';
import CloseShiftModal from '../Shifts/CloseShiftModal';

function StatCard({ label, value, sub, color = 'blue' }) {
  const colors = {
    blue: 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400',
    green: 'bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400',
    yellow: 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-600 dark:text-yellow-400',
    purple: 'bg-purple-50 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400',
  };
  return (
    <div className={`rounded-xl p-5 ${colors[color]}`}>
      <p className="text-xs font-semibold uppercase tracking-wide opacity-70">{label}</p>
      <p className="text-2xl font-bold mt-1">{value}</p>
      {sub && <p className="text-xs mt-1 opacity-60">{sub}</p>}
    </div>
  );
}

export default function DashboardPage({ addToast }) {
  const dispatch = useDispatch();
  const currentShift = useSelector((s) => s.shift.currentShift);
  const sales = useSelector((s) => s.sales.sales);
  const [openShiftOpen, setOpenShiftOpen] = useState(false);
  const [closeShiftOpen, setCloseShiftOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const shiftRes = await getCurrentShift();
      dispatch(setCurrentShift(shiftRes.data));
      if (shiftRes.data?.id) {
        const salesRes = await getSales({ shift: shiftRes.data.id });
        dispatch(setSales(Array.isArray(salesRes.data) ? salesRes.data : salesRes.data.results || []));
      } else {
        dispatch(setSales([]));
      }
    } catch (err) {
      if (err.response?.status !== 404) {
        addToast('Failed to load shift data', 'error');
      }
      dispatch(setCurrentShift(null));
      dispatch(setSales([]));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const totalCash = sales.filter((s) => s.payment_type === 'CASH').reduce((a, s) => a + parseFloat(s.amount || 0), 0);
  const totalLiters = sales.reduce((a, s) => a + parseFloat(s.quantity_liters || 0), 0);
  const avgTransaction = sales.length ? (sales.reduce((a, s) => a + parseFloat(s.amount || 0), 0) / sales.length) : 0;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <ShiftInfo
        onOpenShift={() => setOpenShiftOpen(true)}
        onCloseShift={() => setCloseShiftOpen(true)}
      />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Total Cash" value={`${totalCash.toLocaleString()} RWF`} color="green" />
        <StatCard label="Total Liters" value={`${totalLiters.toFixed(1)} L`} color="blue" />
        <StatCard label="Transactions" value={sales.length} sub="this shift" color="purple" />
        <StatCard label="Avg Transaction" value={`${Math.round(avgTransaction).toLocaleString()} RWF`} color="yellow" />
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5">
        <h2 className="text-sm font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wide mb-4">
          Fuel Sales by Type
        </h2>
        <SalesChart sales={sales} />
      </div>

      {openShiftOpen && (
        <OpenShiftModal
          onClose={() => setOpenShiftOpen(false)}
          onSuccess={(shift) => {
            dispatch(setCurrentShift(shift));
            setOpenShiftOpen(false);
            addToast('Shift opened successfully', 'success');
          }}
        />
      )}

      {closeShiftOpen && currentShift && (
        <CloseShiftModal
          shift={currentShift}
          sales={sales}
          onClose={() => setCloseShiftOpen(false)}
          onSuccess={() => {
            dispatch(setCurrentShift(null));
            dispatch(setSales([]));
            setCloseShiftOpen(false);
            addToast('Shift closed successfully', 'success');
          }}
        />
      )}
    </div>
  );
}
