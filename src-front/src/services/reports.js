import { request } from './requests';

const reportPrefix = '/reports';

export class ReportsService {
  userService;

  constructor(userService) {
    this.userService = userService;
  }

  async getReport(reportType, filters = {}) {
    let reportUrl = `${reportPrefix}/${reportType}/`;


    return await request(reportUrl, {
      method: 'POST',
      body: JSON.stringify(filters),
    }, { userService: this.userService });
  }
}