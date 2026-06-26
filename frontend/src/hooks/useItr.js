import { useState, useCallback } from 'react';
import { getItrReport, getTaxAdvisory } from '../services/api';
import toast from 'react-hot-toast';

export function useItr(userId = null) {
  const [report, setReport] = useState(null);
  const [advisory, setAdvisory] = useState('');
  const [loading, setLoading] = useState(false);
  const [advisoryLoading, setAdvisoryLoading] = useState(false);

  const fetchItrReport = useCallback(async (otherIncome = 0, deductions80c = 150000, deductions80d = 25000, applyPresumptive = false) => {
    if (!userId) return;
    setLoading(true);
    try {
      const res = await getItrReport(userId, otherIncome, deductions80c, deductions80d, applyPresumptive);
      setReport(res.data);
      return res.data;
    } catch (err) {
      toast.error('ITR REPORT AGGREGATION FAILED.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  const fetchAdvisory = useCallback(async (summary) => {
    setAdvisoryLoading(true);
    try {
      const res = await getTaxAdvisory(summary);
      setAdvisory(res.data.advice);
    } catch (err) {
      toast.error('TAX ADVISORY VERDICT FAILED.');
    } finally {
      setAdvisoryLoading(false);
    }
  }, []);

  return {
    report,
    advisory,
    loading,
    advisoryLoading,
    fetchItrReport,
    fetchAdvisory
  };
}
