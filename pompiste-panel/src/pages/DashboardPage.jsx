import DashboardComponent from '../components/Dashboard/DashboardPage';

export default function DashboardPage({ addToast }) {
  return (
    <div>
      <h1 className="text-xl font-bold text-gray-900 dark:text-white mb-5">Dashboard</h1>
      <DashboardComponent addToast={addToast} />
    </div>
  );
}
