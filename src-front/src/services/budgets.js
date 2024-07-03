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

}