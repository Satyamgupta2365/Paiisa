import { useState, useCallback } from 'react';
import { getCashFlow } from '../services/api';
import toast from 'react-hot-toast';

export function useCashFlow(userId = null) {
  const [cashFlow, setCashFlow] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchCashFlow = useCallback(async () => {
    setLoading(true);
    try {
      const res = await getCashFlow(userId);
      setCashFlow(res.data);
    } catch (err) {
      toast.error('CASHFLOW SYNC FAILED.');
    } finally {
      setLoading(false);
    }
  }, [userId]);

  return { cashFlow, loading, fetchCashFlow };
}
