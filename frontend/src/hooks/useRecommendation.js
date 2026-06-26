import { useState } from 'react';
import { getRecommendation, processPayment } from '../services/api';
import toast from 'react-hot-toast';

export function useRecommendation() {
  const [recommendation, setRecommendation] = useState(null);
  const [paymentResult, setPaymentResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchRecommendation = async (amount, category) => {
    setLoading(true);
    setRecommendation(null);
    setPaymentResult(null);
    try {
      const res = await getRecommendation(amount, category);
      setRecommendation(res.data);
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to fetch recommendation");
    } finally {
      setLoading(false);
    }
  };

  const executePayment = async (userId, method, amount, category) => {
    setLoading(true);
    try {
      const res = await processPayment(userId, method, amount, category);
      setPaymentResult(res.data);
      if (res.data.status === 'success') {
        toast.success(`Payment successful! Earned ₹${res.data.cashback_earned}`);
      } else {
        toast.error("Payment failed");
      }
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to process payment");
    } finally {
      setLoading(false);
    }
  };

  return { recommendation, paymentResult, loading, fetchRecommendation, executePayment, setRecommendation, setPaymentResult };
}
