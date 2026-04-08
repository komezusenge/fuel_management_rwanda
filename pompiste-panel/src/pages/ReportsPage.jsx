import DailySalesReport from '../components/Reports/DailySalesReport';
import ShiftHistory from '../components/Shifts/ShiftHistory';

export default function ReportsPage({ addToast }) {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-xl font-bold text-gray-900 dark:text-white mb-5">Daily Sales Report</h1>
        <DailySalesReport addToast={addToast} />
      </div>
      <div>
        <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-4">Shift History</h2>
        <ShiftHistory addToast={addToast} />
      </div>
    </div>
  );
}
