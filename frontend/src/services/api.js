import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  headers: { 'Content-Type': 'application/json' }
});

// ── Smart Payment Routing ──────────────────────────────────────────────────────
export const getRecommendation = (amount, category, userId = null) =>
  api.post('/recommend-payment', { amount: parseFloat(amount), category, user_id: userId });

export const processPayment = (userId, paymentMethod, amount, category = null) =>
  api.post('/process-payment', { user_id: userId, payment_method: paymentMethod, amount: parseFloat(amount), category });

// ── Offers ─────────────────────────────────────────────────────────────────────
export const getOffers = () => api.get('/offers');
export const createOffer = (data) => api.post('/offers', data);
export const deleteOffer = (id) => api.delete(`/offers/${id}`);

// ── Users ──────────────────────────────────────────────────────────────────────
export const createUser = (data) => api.post('/users', data);
export const getUser = (userId) => api.get(`/users/${userId}`);
export const getTransactions = (userId) => api.get(`/users/${userId}/transactions`);
export const getInsights = (userId) => api.get(`/users/${userId}/insights`);

// ── Travel Guardian (Pillar 1 — All 5 Features) ───────────────────────────────
export const scanTravel = (destination = 'Tokyo, Japan', userId = null) =>
  api.post('/travel/scan', { destination, user_id: userId });

export const fixTravel = (userId = null, destination = 'Tokyo, Japan') =>
  api.post('/travel/fix', { user_id: userId, destination });

/** Salary affordability — plain text version */
export const analyzeSalaryAffordability = (salaryText, destination = 'Tokyo, Japan', tripCost = 80000) =>
  api.post('/travel/affordability', {
    salary_text: salaryText,
    destination,
    trip_cost: tripCost,
  });

/** Salary affordability — file upload version */
export const analyzeSalaryFile = (formData) =>
  axios.post(
    (process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1') + '/travel/affordability/upload',
    formData,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  );

/** Trip Budget Planner — AI-generated itemised budget */
export const planTripBudget = (destination = 'Tokyo, Japan', durationDays = 7, tripBudget = 83000) =>
  api.post('/travel/budget', {
    destination,
    duration_days: durationDays,
    trip_budget: tripBudget,
  });

/** Emergency Virtual Card — 24-hour RuPay International card */
export const generateVirtualCard = (userName = 'Traveller', amount = 25000, destination = 'Tokyo, Japan') =>
  api.post('/travel/emergency-card', {
    user_name: userName,
    amount,
    destination,
  });

// ── Cash Flow Predictor (Pillar 3) ─────────────────────────────────────────────
export const getCashFlow = (userId) =>
  userId ? api.get(`/merchant/cashflow/${userId}`) : api.get('/merchant/cashflow/demo/mock');

// ── TAP Server (Pillar 5) ──────────────────────────────────────────────────────
export const getTapRules = (userId) => api.get(`/tap/rules/${userId}`);
export const updateTapRules = (userId, rules) => api.put(`/tap/rules/${userId}`, rules);
export const submitTapRequest = (data) => api.post('/tap/request', data);
export const getTapLogs = (userId) => api.get(`/tap/logs/${userId}`);

// ── Merchant Bank Statement Analyzer (Groq AI) ────────────────────────────────
/** Analyze pasted bank statement text */
export const analyzeStatement = (statementText, companyName = 'My Business') =>
  api.post('/merchant/analyze-statement', {
    statement_text: statementText,
    company_name: companyName,
  });

/** Upload bank statement file */
export const analyzeStatementFile = (formData) =>
  axios.post(
    (process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1') + '/merchant/analyze-statement/upload',
    formData,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  );

/** Instant demo analysis — uses the company name the user entered */
export const analyzeStatementDemo = (companyName = 'My Business') =>
  api.post(`/merchant/analyze-statement/demo?company_name=${encodeURIComponent(companyName)}`);

/** Get all past analyses (history) */
export const getStatementHistory = () =>
  api.get('/merchant/statement-history');

/** Re-load a specific past analysis by ID */
export const getStatementById = (id) =>
  api.get(`/merchant/statement-history/${id}`);

// ── ITR Tax Filing ─────────────────────────────────────────────────────────────
export const getItrReport = (userId, otherIncome = 0, deductions80c = 150000, deductions80d = 25000, applyPresumptive = true) =>
  api.get(`/itr/report/${userId}`, {
    params: {
      other_income: parseFloat(otherIncome),
      deductions_80c: parseFloat(deductions80c),
      deductions_80d: parseFloat(deductions80d),
      apply_presumptive_44ad: applyPresumptive,
    }
  });

export const getItrReportDemo = (otherIncome = 0, deductions80c = 150000, deductions80d = 25000, applyPresumptive = true) =>
  api.get('/itr/report/demo', {
    params: {
      other_income: parseFloat(otherIncome),
      deductions_80c: parseFloat(deductions80c),
      deductions_80d: parseFloat(deductions80d),
      apply_presumptive_44ad: applyPresumptive,
    }
  });

export const getTaxAdvisory = (summary) => api.post('/itr/advise', { summary });


