import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';

const FUEL_COLORS = {
  PETROL: '#3b82f6',
  DIESEL: '#10b981',
  SUPER: '#f59e0b',
};

export default function SalesChart({ sales }) {
  const aggregated = sales.reduce((acc, sale) => {
    const ft = sale.fuel_type;
    if (!acc[ft]) acc[ft] = { fuel_type: ft, liters: 0, amount: 0 };
    acc[ft].liters += parseFloat(sale.quantity_liters || 0);
    acc[ft].amount += parseFloat(sale.amount || 0);
    return acc;
  }, {});

  const data = Object.values(aggregated);

  if (!data.length) {
    return (
      <div className="flex items-center justify-center h-48 text-gray-400 dark:text-gray-500 text-sm">
        No sales data for this shift
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={220}>
      <BarChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
        <XAxis dataKey="fuel_type" tick={{ fontSize: 12 }} />
        <YAxis yAxisId="left" tick={{ fontSize: 12 }} />
        <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 12 }} />
        <Tooltip
          formatter={(value, name) =>
            name === 'liters'
              ? [`${Number(value).toFixed(2)} L`, 'Liters']
              : [`${Number(value).toLocaleString()} RWF`, 'Amount']
          }
        />
        <Legend />
        <Bar yAxisId="left" dataKey="liters" name="Liters" fill="#3b82f6" radius={[4, 4, 0, 0]} />
        <Bar yAxisId="right" dataKey="amount" name="Amount (RWF)" fill="#10b981" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
