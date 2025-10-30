# CLAUDE.md - Frontend

This file provides guidance to Claude Code when working with the Vue.js frontend of the Budget Tracker application.

## Development Commands

### Running the Application
```bash
npm install          # Install dependencies
npm run dev          # Start Vite dev server on :5173
npm run build        # Build for production
npm run preview      # Preview production build
```

### Code Quality
```bash
npm run lint         # Run ESLint
npm run format       # Format code with Prettier
```

## Architecture Overview

### Tech Stack
- **Framework**: Vue 3 (Composition API with `<script setup>`)
- **Build Tool**: Vite
- **State Management**: Pinia
- **Routing**: Vue Router 4
- **HTTP Client**: Axios
- **UI Framework**: Bootstrap 5
- **Charts**: Chart.js + vue-chartjs
- **Internationalization**: Vue I18n (English, Ukrainian)
- **Icons**: Font Awesome 6 (use `fa-solid`, `fa-regular` classes)

### Project Structure

```
src-front/
├── src/
│   ├── assets/              # Static assets (images, styles)
│   │   └── scss/            # Custom SCSS styles
│   ├── components/          # Reusable Vue components
│   │   ├── accounts/        # Account-related components
│   │   ├── budgets/         # Budget components
│   │   ├── cards/           # Card UI components
│   │   ├── filters/         # Filter components
│   │   ├── planning/        # Financial planning components
│   │   ├── reports/         # Report components
│   │   ├── transactions/    # Transaction components
│   │   └── utils/           # Utility components (Loader, ConfirmDialog, etc.)
│   ├── views/               # Page-level components (routes)
│   │   ├── accounts/        # Account views
│   │   ├── budgets/         # Budget views
│   │   ├── reports/         # Report views
│   │   └── transactions/    # Transaction views
│   ├── stores/              # Pinia stores
│   ├── services/            # API service layer
│   ├── router/              # Vue Router configuration
│   ├── locales/             # i18n translation files
│   ├── utils/               # Utility functions
│   ├── App.vue              # Root component
│   └── main.js              # Application entry point
├── public/                  # Public static files
├── index.html               # HTML template
├── vite.config.js           # Vite configuration
└── package.json             # Dependencies
```

## Key Components

### Stores (Pinia)

Located in `src/stores/`:

#### authStore (`authStore.js`)
- Manages authentication state
- Handles JWT token storage and refresh
- User login/logout/registration
- Google OAuth integration

#### accountsStore (`accountsStore.js`)
- CRUD operations for accounts
- Account balance tracking
- Account list management
- Credit account handling

#### transactionsStore (`transactionsStore.js`)
- Transaction CRUD operations
- Transaction filtering and pagination
- Income, expense, and transfer types
- Transaction templates

#### plannedTransactionsStore (`plannedTransactions.js`)
- Planned/future transactions
- Recurring transaction rules
- Balance projections
- Financial planning data

#### categoriesStore (`categoriesStore.js`)
- Category management
- Default and user categories
- Expense/income category types

#### currenciesStore (`currenciesStore.js`)
- Currency list
- Exchange rates
- Base currency management

#### budgetsStore (`budgetsStore.js`)
- Budget CRUD operations
- Budget tracking by category
- Monthly budget summaries

### Services (API Layer)

Located in `src/services/`:

All services use Axios for HTTP requests and include:
- Automatic JWT token injection
- Error handling
- Request/response interceptors

#### Key Services:
- `authService.js` - Authentication endpoints
- `accountsService.js` - Account management
- `transactionsService.js` - Transaction operations
- `plannedTransactions.js` - Financial planning API
- `categoriesService.js` - Category management
- `currenciesService.js` - Currency and exchange rates
- `budgetsService.js` - Budget operations
- `reportsService.js` - Report generation

### Views (Pages)

Located in `src/views/`:

#### Main Views:
- **HomeView.vue** - Dashboard with account summaries and quick stats
- **AccountsListView.vue** - List of all accounts with balances
- **AccountDetailsView.vue** - Single account view with transactions
- **TransactionsListView.vue** - All transactions with filtering
- **TransactionNewView.vue** - Create/edit transactions
- **BudgetsView.vue** - Budget management and tracking
- **FinancialPlanningView.vue** - Planned transactions and projections
- **ReportsView.vue** - Reports dashboard
- **BalanceReportView.vue** - Balance over time chart
- **CashFlowReportView.vue** - Income vs expenses
- **ExpenseCategorizationReportView.vue** - Expense breakdown by category
- **SpendingTrendsReportView.vue** - Spending patterns analysis
- **ExpensesReportView.vue** - Detailed expense report with AI insights
- **Settings.vue** - User settings and preferences
- **LoginView.vue** - Login page
- **RegisterView.vue** - Registration page

### Reusable Components

Located in `src/components/`:

#### Account Components (`accounts/`)
- `AccountCard.vue` - Display account summary
- `AccountForm.vue` - Create/edit account form

#### Transaction Components (`transactions/`)
- `TransactionCard.vue` - Transaction display card
- `TransactionForm.vue` - Transaction create/edit form
- `TransactionFilters.vue` - Filter transactions

#### Planning Components (`planning/`)
- `PlannedTransactionModal.vue` - Create/edit planned transactions
- `BalanceProjectionChart.vue` - Future balance visualization
- `UpcomingTransactionsList.vue` - List of upcoming transactions
- `StatisticsPanel.vue` - Financial statistics display

#### Budget Components (`budgets/`)
- `BudgetCard.vue` - Budget display card
- `BudgetForm.vue` - Budget create/edit form
- `BudgetProgressBar.vue` - Visual budget progress

#### Report Components (`reports/`)
- Various chart and table components for reports

#### Utility Components (`utils/`)
- `Loader.vue` - Loading spinner
- `ConfirmDialog.vue` - Confirmation modal
- `ErrorMessage.vue` - Error display
- `Pagination.vue` - Pagination controls

## Key Patterns and Conventions

### Composition API with Script Setup
All components use Vue 3 Composition API with `<script setup>` syntax:

```vue
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from '@/stores/myStore'

const store = useStore()
const data = ref([])

onMounted(async () => {
  await store.loadData()
})
</script>
```

### Store Pattern
- Stores handle all state management and API calls
- Components consume store data via computed properties
- Actions return promises for async operations

### Service Layer
- Services encapsulate all API communication
- Use Axios with interceptors for auth and error handling
- Return promises that resolve to response data

### Component Communication
- Props for parent-to-child data flow
- Events for child-to-parent communication
- Stores for shared state across components

### Routing and Navigation Guards
- Router configured in `src/router/index.js`
- Navigation guards check authentication state
- Redirects to login if not authenticated

### Internationalization
- Translation files in `src/locales/` (en.json, uk.json)
- Use `$t('key')` in templates
- Use `t('key')` in script setup with `useI18n()`

### Styling
- Bootstrap 5 for base styles
- Custom SCSS in `src/assets/scss/`
- Scoped styles in components
- Bootstrap Icons for iconography

## API Integration

### Base URL Configuration
Set in `.env` file:
```env
VITE_API_URL=http://localhost:8000/api/v1
```

### Authentication Flow
1. User logs in via `authService.login()`
2. JWT token stored in `authStore`
3. Token automatically included in all API requests
4. Token refresh handled by middleware
5. Logout clears token and redirects to login

### Error Handling
- API errors caught in services
- Error messages displayed via toast notifications
- 401 errors trigger automatic logout
- Validation errors shown in forms

## State Management with Pinia

### Store Structure
```javascript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useMyStore = defineStore('myStore', () => {
  // State
  const items = ref([])

  // Getters
  const itemCount = computed(() => items.value.length)

  // Actions
  async function fetchItems() {
    const data = await myService.getItems()
    items.value = data
  }

  return { items, itemCount, fetchItems }
})
```

### Store Usage in Components
```vue
<script setup>
import { useMyStore } from '@/stores/myStore'

const store = useMyStore()

// Access state
console.log(store.items)

// Call actions
await store.fetchItems()
</script>
```

## Deployment

### Building for Production
```bash
npm run build
```

This creates optimized static files in `dist/` directory.

### Docker Build
```bash
./build-frontend-docker.sh
```

This script:
1. Builds production bundle
2. Creates Docker image with Nginx
3. Pushes to Docker Hub

### Environment Variables
Production `.env`:
```env
VITE_API_URL=https://api.yourdomain.com/api/v1
VITE_GOOGLE_CLIENT_ID=your-google-client-id
```

## Common Development Tasks

### Add New Page/View
1. Create component in `src/views/`
2. Add route in `src/router/index.js`
3. Add navigation link in menu components
4. Create corresponding API service if needed
5. Update store if needed

### Add New Component
1. Create `.vue` file in appropriate `src/components/` subdirectory
2. Use Composition API with `<script setup>`
3. Add props, events, and local state as needed
4. Import and use in parent components

### Add New Store
1. Create file in `src/stores/`
2. Define state, getters, and actions
3. Export with `defineStore`
4. Import and use in components

### Add New API Service
1. Create file in `src/services/`
2. Import axios instance
3. Define API methods returning promises
4. Use in store actions

### Add Translation
1. Add key-value pairs to `src/locales/en.json`
2. Add corresponding Ukrainian translations to `src/locales/uk.json`
3. Use in templates: `{{ $t('key') }}`
4. Use in script: `const { t } = useI18n(); t('key')`

## Troubleshooting

### Development Server Issues
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check Vite config in `vite.config.js`
- Verify API URL in `.env`

### API Connection Issues
- Verify backend is running
- Check VITE_API_URL in `.env`
- Check browser console for CORS errors
- Verify JWT token in localStorage

### State Management Issues
- Check Pinia store state in Vue DevTools
- Verify store actions are awaited
- Check for proper store initialization

### Routing Issues
- Verify route definitions in router
- Check navigation guards
- Clear browser history/cache

## Testing

### Unit Tests
```bash
npm run test:unit
```

### E2E Tests
```bash
npm run test:e2e
```

## Best Practices

1. **Use Composition API** - Prefer `<script setup>` syntax
2. **Type Safety** - Use JSDoc comments for better IDE support
3. **Component Size** - Keep components focused and small
4. **Store Actions** - Always use stores for API calls
5. **Error Handling** - Always handle promise rejections
6. **Loading States** - Show loading indicators for async operations
7. **Validation** - Validate forms before submission
8. **Accessibility** - Use semantic HTML and ARIA attributes
9. **Responsive Design** - Test on mobile, tablet, and desktop
10. **Performance** - Use computed properties for derived data
11. **Code Organization** - Group related components in subdirectories
12. **Naming Conventions** - Use PascalCase for components, camelCase for variables
