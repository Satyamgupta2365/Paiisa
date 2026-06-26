import { useState, useCallback } from 'react';
import { getTapRules, updateTapRules, submitTapRequest, getTapLogs } from '../services/api';
import toast from 'react-hot-toast';

export function useTap(userId) {
  const [rules, setRules] = useState(null);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchRules = useCallback(async () => {
    if (!userId) return;
    setLoading(true);
    try {
      const res = await getTapRules(userId);
      setRules(res.data);
    } catch (err) {
      toast.error('RULES FETCH FAILED.');
    } finally {
      setLoading(false);
    }
  }, [userId]);

  const saveRules = useCallback(async (ruleData) => {
    if (!userId) return;
    setLoading(true);
    try {
      const res = await updateTapRules(userId, ruleData);
      setRules(res.data);
      toast.success('FINANCIAL CONSTITUTION UPDATED.');
    } catch (err) {
      toast.error('CONSTITUTION UPDATE FAILED.');
    } finally {
      setLoading(false);
    }
  }, [userId]);

  const simulatePing = useCallback(async (agentId, amount, category = 'food', merchantId = null) => {
    if (!userId) {
      toast.error('AUTH REQUIRED TO SIMULATE.');
      return;
    }
    try {
      const res = await submitTapRequest({
        user_id: userId,
        agent_id: agentId,
        amount,
        category,
        merchant_id: merchantId,
      });
      // Refresh logs after each request
      const logsRes = await getTapLogs(userId);
      setLogs(logsRes.data);
      return res.data;
    } catch (err) {
      toast.error('TAP REQUEST FAILED');
    }
  }, [userId]);

  const fetchLogs = useCallback(async () => {
    if (!userId) return;
    try {
      const res = await getTapLogs(userId);
      setLogs(res.data);
    } catch (err) {
      // silently fail — logs may be empty
    }
  }, [userId]);

  return { rules, logs, loading, fetchRules, saveRules, simulatePing, fetchLogs };
}
