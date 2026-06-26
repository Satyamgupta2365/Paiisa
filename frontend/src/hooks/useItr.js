import { useState, useCallback } from 'react';
import { getItrReport, getItrReportDemo, getTaxAdvisory } from '../services/api';
import toast from 'react-hot-toast';

export function useItr(userId = null) {
  const [report, setReport] = useState(null);
  const [advisory, setAdvisory] = useState('');
  const [loading, setLoading] = useState(false);
  const [advisoryLoading, setAdvisoryLoading] = useState(false);

  const fetchItrReport = useCallback(async (
    otherIncome = 0,
    deductions80c = 150000,
    deductions80d = 25000,
    applyPresumptive = true
  ) => {
    setLoading(true);
    try {
      let res;
      if (userId) {
        res = await getItrReport(userId, otherIncome, deductions80c, deductions80d, applyPresumptive);
      } else {
        // Use demo endpoint when not logged in — pulls data from DB regardless
        res = await getItrReportDemo(otherIncome, deductions80c, deductions80d, applyPresumptive);
      }
      setReport(res.data);
      return res.data;
    } catch (err) {
      const detail = err?.response?.data?.detail || err?.message || 'Unknown error';
      toast.error(`ITR AGGREGATION ERROR: ${detail}`);
      console.error('[useItr] Error:', err);
      return null;
    } finally {
      setLoading(false);
    }
  }, [userId]);

  const fetchAdvisory = useCallback(async (summary) => {
    if (!summary) return;
    setAdvisoryLoading(true);
    try {
      const res = await getTaxAdvisory(summary);
      setAdvisory(res.data.advice);
    } catch (err) {
      toast.error('TAX ADVISORY FAILED. CHECK API CONNECTION.');
      console.error('[useItr] Advisory error:', err);
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
    fetchAdvisory,
    setReport,
  };
}
