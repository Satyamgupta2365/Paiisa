import { useState, useEffect } from 'react';
import { getInsights, getTransactions } from '../services/api';

export function useInsights(userId) {
  const [insights, setInsights] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!userId) return;
    
    let isMounted = true;
    const fetchData = async () => {
      setLoading(true);
      try {
        const [insightsRes, txnsRes] = await Promise.all([
          getInsights(userId),
          getTransactions(userId)
        ]);
        if (isMounted) {
          setInsights(insightsRes.data);
          setTransactions(txnsRes.data);
        }
      } catch (err) {
        console.error("Failed to load insights:", err);
      } finally {
        if (isMounted) setLoading(false);
      }
    };
    
    fetchData();
    return () => { isMounted = false; };
  }, [userId]);

  return { insights, transactions, loading };
}
