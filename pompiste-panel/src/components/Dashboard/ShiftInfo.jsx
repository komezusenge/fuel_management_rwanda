import { useSelector } from 'react-redux';
import dayjs from 'dayjs';

export default function ShiftInfo({ onOpenShift, onCloseShift }) {
  const currentShift = useSelector((s) => s.shift.currentShift);

  if (!currentShift) {
    return (
      <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-700 rounded-xl p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-yellow-100 dark:bg-yellow-800 rounded-full flex items-center justify-center">
            <svg className="w-5 h-5 text-yellow-600 dark:text-yellow-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a1 1 0 00.86 1.5h18.64a1 1 0 00.86-1.5L12.71 3.86a1 1 0 00-1.42 0z" />
            </svg>
          </div>
          <div>
            <p className="font-semibold text-yellow-800 dark:text-yellow-300">No active shift</p>
            <p className="text-sm text-yellow-600 dark:text-yellow-400">Open a shift to start recording sales</p>
          </div>
        </div>
        <button
          onClick={onOpenShift}
          className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold rounded-lg transition-colors"
        >
          Open Shift
        </button>
      </div>
    );
  }

  return (
    <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-700 rounded-xl p-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-green-100 dark:bg-green-800 rounded-full flex items-center justify-center">
            <span className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
          </div>
          <div>
            <p className="font-semibold text-green-800 dark:text-green-300">
              Shift Active — Pump {currentShift.pump}
            </p>
            <p className="text-sm text-green-600 dark:text-green-400">
              Opened {dayjs(currentShift.created_at).format('DD MMM YYYY HH:mm')}
            </p>
          </div>
        </div>

        <div className="flex flex-wrap gap-4 text-sm">
          <div>
            <p className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">Fuel</p>
            <p className="font-medium text-gray-800 dark:text-gray-200">{currentShift.fuel_type}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">Opening Meter</p>
            <p className="font-medium text-gray-800 dark:text-gray-200">{Number(currentShift.opening_meter).toLocaleString()} L</p>
          </div>
          <div>
            <p className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">Starting Cash</p>
            <p className="font-medium text-gray-800 dark:text-gray-200">{Number(currentShift.starting_cash).toLocaleString()} RWF</p>
          </div>
        </div>

        <button
          onClick={onCloseShift}
          className="px-5 py-2.5 bg-red-600 hover:bg-red-700 text-white text-sm font-semibold rounded-lg transition-colors self-start sm:self-auto"
        >
          Close Shift
        </button>
      </div>
    </div>
  );
}
