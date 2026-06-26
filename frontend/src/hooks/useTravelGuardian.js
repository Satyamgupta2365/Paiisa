import { useState, useCallback } from 'react';
import {
  scanTravel, fixTravel,
  analyzeSalaryAffordability, analyzeSalaryFile,
  planTripBudget, generateVirtualCard,
} from '../services/api';
import toast from 'react-hot-toast';

export function useTravelGuardian() {
  const [scanResult, setScanResult]             = useState(null);
  const [affordability, setAffordability]       = useState(null);
  const [budget, setBudget]                     = useState(null);
  const [virtualCard, setVirtualCard]           = useState(null);
  const [loading, setLoading]                   = useState(false);
  const [affordabilityLoading, setAffLoading]   = useState(false);
  const [budgetLoading, setBudgetLoading]       = useState(false);
  const [cardLoading, setCardLoading]           = useState(false);

  // ── 1. Pre-departure scan ────────────────────────────────────────────────────
  const scan = useCallback(async (destination = 'Tokyo, Japan', userId = null) => {
    setLoading(true);
    try {
      const res = await scanTravel(destination, userId);
      setScanResult(res.data);
    } catch {
      toast.error('TRAVEL SCAN FAILED — BACKEND ERROR');
    } finally {
      setLoading(false);
    }
  }, []);

  // ── 2. One-tap Fix All ───────────────────────────────────────────────────────
  const fix = useCallback(async (userId = null, destination = 'Tokyo, Japan') => {
    setLoading(true);
    try {
      const res = await fixTravel(userId, destination);
      setScanResult(res.data);
      toast.success('GUARDIAN.PROTOCOL: ALL SYSTEMS SECURED ✓');
    } catch {
      toast.error('FIX PROTOCOL FAILED.');
    } finally {
      setLoading(false);
    }
  }, []);

  // ── 3. Salary Affordability (text) ──────────────────────────────────────────
  const analyzeSalary = useCallback(async (salaryText, destination, tripCost) => {
    setAffLoading(true);
    try {
      const res = await analyzeSalaryAffordability(salaryText, destination, tripCost);
      setAffordability(res.data);
    } catch {
      toast.error('GROQ AI ANALYSIS FAILED.');
    } finally {
      setAffLoading(false);
    }
  }, []);

  // ── 3b. Salary Affordability (file upload) ───────────────────────────────────
  const analyzeSalaryFromFile = useCallback(async (file, destination, tripCost) => {
    setAffLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('destination', destination);
      formData.append('trip_cost', String(tripCost));
      const res = await analyzeSalaryFile(formData);
      setAffordability(res.data);
    } catch {
      toast.error('FILE UPLOAD ANALYSIS FAILED.');
    } finally {
      setAffLoading(false);
    }
  }, []);

  // ── 4. Budget Planner ────────────────────────────────────────────────────────
  const planBudget = useCallback(async (destination, durationDays, tripBudget) => {
    setBudgetLoading(true);
    try {
      const res = await planTripBudget(destination, durationDays, tripBudget);
      setBudget(res.data);
    } catch {
      toast.error('BUDGET PLANNER FAILED.');
    } finally {
      setBudgetLoading(false);
    }
  }, []);

  // ── 5. Emergency Virtual Card ────────────────────────────────────────────────
  const getVirtualCard = useCallback(async (userName = 'Traveller', amount = 25000, destination = 'Tokyo, Japan') => {
    setCardLoading(true);
    try {
      const res = await generateVirtualCard(userName, amount, destination);
      setVirtualCard(res.data);
      toast.success('EMERGENCY CARD ACTIVATED');
    } catch {
      toast.error('VIRTUAL CARD GENERATION FAILED.');
    } finally {
      setCardLoading(false);
    }
  }, []);

  return {
    scanResult, affordability, budget, virtualCard,
    loading, affordabilityLoading, budgetLoading, cardLoading,
    scan, fix, analyzeSalary, analyzeSalaryFromFile, planBudget, getVirtualCard,
  };
}
