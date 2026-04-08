import { useState, useCallback } from 'react';
import { getCustomers } from '../../services/customerService';
import debounce from './debounce';

export default function CustomerLookup({ onSelect, selected }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const search = useCallback(
    debounce(async (q) => {
      if (!q.trim()) { setResults([]); return; }
      setLoading(true);
      try {
        const res = await getCustomers({ search: q });
        setResults(Array.isArray(res.data) ? res.data : res.data.results || []);
      } catch {
        setResults([]);
      } finally {
        setLoading(false);
      }
    }, 300),
    []
  );

  const handleChange = (e) => {
    setQuery(e.target.value);
    search(e.target.value);
  };

  return (
    <div className="relative">
      <div className="relative">
        <input
          type="text"
          value={selected ? `${selected.name}${selected.phone ? ` (${selected.phone})` : ''}` : query}
          onChange={handleChange}
          onFocus={() => selected && onSelect(null)}
          placeholder="Search by name or phone…"
          className="w-full px-4 py-2.5 pr-10 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {loading && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2">
            <div className="animate-spin w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full" />
          </div>
        )}
      </div>

      {results.length > 0 && !selected && (
        <ul className="absolute z-10 mt-1 w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg max-h-48 overflow-y-auto">
          {results.map((c) => (
            <li key={c.id}>
              <button
                type="button"
                onClick={() => { onSelect(c); setQuery(''); setResults([]); }}
                className="w-full px-4 py-2.5 text-left text-sm hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-900 dark:text-white"
              >
                <span className="font-medium">{c.name}</span>
                {c.phone && <span className="text-gray-500 dark:text-gray-400 ml-2">{c.phone}</span>}
                {c.balance !== undefined && (
                  <span className={`ml-2 text-xs ${c.balance < 0 ? 'text-red-500' : 'text-green-500'}`}>
                    {Number(c.balance).toLocaleString()} RWF
                  </span>
                )}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
