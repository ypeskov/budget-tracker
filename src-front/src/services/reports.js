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

  async getDiagram(reportType, startDate, endDate) {
    const reportUrl = `http://localhost:8000${reportPrefix}/diagram/${reportType}/${startDate}/${endDate}`;
    const token = localStorage.getItem('accessToken');

    const response = await fetch(reportUrl, {
      headers: {
        'auth-token': token,
    },

    });

    if (!response.ok) {
      throw new Error('Failed to fetch diagram');
    }

    const blob = await response.blob();
    return URL.createObjectURL(blob);
  }
}