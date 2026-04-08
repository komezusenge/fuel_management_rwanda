# Pompiste Panel — Fuel Management Rwanda

A modern, responsive React-based panel for pump attendants (pompistes) to manage fuel sales, shifts, and daily operations.

## Features

- 🔐 **Authentication** — JWT login/logout with auto-refresh and auto-logout on expiry
- ⛽ **Shift Management** — Open/close shifts, shift history
- 💰 **Sales Recording** — Cash & credit sales, receipt printing, offline queue
- 📊 **Dashboard** — Real-time stats, fuel breakdown chart, quick actions
- 📈 **Reports** — Daily sales report with CSV export
- 👥 **Customer Management** — Credit customer lookup and transactions
- 🌙 **Dark/Light Mode** — Persisted in localStorage
- 📱 **Offline Support** — Sales queued locally and synced when back online

## Tech Stack

- **React 19** + **Vite**
- **Redux Toolkit** — state management (auth, sales, shift)
- **Axios** — HTTP client with JWT Bearer interceptor and 401 auto-refresh
- **React Router v6** — client-side routing with protected routes
- **Tailwind CSS v3** — utility-first styling
- **Recharts** — sales bar chart
- **React Hook Form** — form handling
- **Day.js** — date/time utilities

## Getting Started

### Prerequisites

- Node.js 18+
- The Django backend running at `http://localhost:8000/api/`

### Installation

```bash
cd pompiste-panel
npm install
```

### Environment

```bash
cp .env.example .env
```

Edit `.env` if your API runs on a different URL:

```
VITE_API_BASE_URL=http://localhost:8000/api
```

### Development

```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

### Production Build

```bash
npm run build
npm run preview
```

## Usage

1. Log in with your pompiste credentials (email + password)
2. Open a shift: select pump, tank, fuel type, enter starting cash and opening meter
3. Record sales throughout the shift
4. Close the shift at end of day with closing meter and cash count
5. View daily reports and export to CSV

## Project Structure

```
src/
├── components/
│   ├── Auth/           LoginPage, LogoutButton
│   ├── Common/         Header, Navigation, NotificationToast
│   ├── Customers/      CustomerLookup, CreditTransactions
│   ├── Dashboard/      DashboardPage, ShiftInfo, SalesChart
│   ├── Reports/        DailySalesReport, ReportExporter
│   ├── Sales/          SalesEntry, SalesHistory, ReceiptPrinter
│   └── Shifts/         OpenShiftModal, CloseShiftModal, ShiftHistory
├── pages/              DashboardPage, SalesPage, ReportsPage, ProfilePage
├── services/           api.js, authService, salesService, shiftService, customerService
└── store/              store.js, authSlice, salesSlice, shiftSlice
```

## API Endpoints (Django Backend)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login/` | Obtain JWT tokens |
| POST | `/api/auth/logout/` | Blacklist refresh token |
| POST | `/api/auth/refresh/` | Refresh access token |
| GET | `/api/users/me/` | Current user profile |
| GET/POST | `/api/pumps/shifts/` | List / create shift |
| POST | `/api/pumps/shifts/{id}/close/` | Close shift |
| GET/POST | `/api/sales/` | List / create sale |
| GET | `/api/sales/prices/` | Current fuel prices |
| GET | `/api/customers/` | List customers |
| POST | `/api/customers/transactions/` | Credit transaction |
| GET | `/api/reports/daily/` | Daily sales report |
