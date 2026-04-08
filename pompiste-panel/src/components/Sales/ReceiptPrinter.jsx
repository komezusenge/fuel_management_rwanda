import dayjs from 'dayjs';

export default function ReceiptPrinter({ sale, onClose }) {
  const handlePrint = () => window.print();

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-full max-w-sm p-6">
        <div className="text-center mb-4 border-b border-gray-200 dark:border-gray-700 pb-4">
          <h2 className="font-bold text-lg text-gray-900 dark:text-white">Sales Receipt</h2>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
            {dayjs(sale.created_at).format('DD MMM YYYY HH:mm:ss')}
          </p>
        </div>

        <dl className="space-y-2 text-sm mb-4">
          {[
            ['Receipt #', sale.id],
            ['Fuel Type', sale.fuel_type],
            ['Quantity', `${Number(sale.quantity_liters).toFixed(2)} L`],
            ['Amount', `${Number(sale.amount).toLocaleString()} RWF`],
            ['Payment', sale.payment_type],
            ...(sale.customer_name || sale.customer ? [['Customer', sale.customer_name || sale.customer]] : []),
          ].map(([label, value]) => (
            <div key={label} className="flex justify-between">
              <dt className="text-gray-500 dark:text-gray-400">{label}</dt>
              <dd className="font-medium text-gray-900 dark:text-white">{value}</dd>
            </div>
          ))}
        </dl>

        <div className="border-t border-dashed border-gray-300 dark:border-gray-600 pt-3 text-center">
          <p className="text-xs text-gray-400 dark:text-gray-500">Thank you for your business</p>
        </div>

        <div className="flex gap-3 mt-5">
          <button
            onClick={handlePrint}
            className="flex-1 py-2.5 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm font-medium"
          >
            Print
          </button>
          <button
            onClick={onClose}
            className="flex-1 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors text-sm font-semibold"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
}
