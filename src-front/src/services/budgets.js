import { request } from './requests';

const budgetsPrefix = '/budgets';

export class BudgetsService {
  userService;

  constructor(userService) {
    this.userService = userService;
  }

  async getUserBudgets() {
    let budgetUrl = `${budgetsPrefix}/`;

    return await request(budgetUrl, {}, { userService: this.userService });
  }

  async createBudget(budget) {
    let budgetUrl = `${budgetsPrefix}/add/`;

    return await request(budgetUrl, {
      method: 'POST',
      body: JSON.stringify(budget),
    }, { userService: this.userService });
  }

  async updateBudget(budget) {
    let budgetUrl = `${budgetsPrefix}/${budget.id}/`;

    return await request(budgetUrl, {
      method: 'PUT',
      body: JSON.stringify(budget),
    }, { userService: this.userService });
  }
}