export default function ReportExporter({ report, date }) {
  const exportCSV = () => {
    const rows = [
      ['Date', date],
      ['Total Amount (RWF)', report.total_amount || 0],
      ['Total Liters', report.total_liters || 0],
      ['Cash (RWF)', report.cash_amount || 0],
      ['Credit (RWF)', report.credit_amount || 0],
      [],
      ['Fuel Type', 'Liters', 'Amount (RWF)', 'Transactions'],
    ];

    Object.entries(report.fuel_breakdown || {}).forEach(([ft, data]) => {
      rows.push([ft, data.liters || 0, data.amount || 0, data.count || 0]);
    });

    const csv = rows.map((r) => r.map((v) => `"${v}"`).join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `fuel_report_${date}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <button
      onClick={exportCSV}
      className="flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm font-medium"
    >
      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
      </svg>
      Export CSV
    </button>
  );
}
