import { useUserStore } from "../stores/user";
import { useAccountStore } from "../stores/account";

export class AccountService {
  userStore;
  accountStore;
  
  constructor() {
    this.userStore = useUserStore();
    this.accountStore = useAccountStore();
  }

  async getAllUserAccounts() {
    const accountsUrl = 'http://localhost:9000/accounts';
    const requestHeaders = {
      'Content-Type': 'application/json',
      'auth-token': this.userStore.accessToken
    };

    const response = await fetch(accountsUrl, { headers: requestHeaders });
    if (response.status === 200) {
      try {
        const accs = await response.json();
        this.accountStore.accounts.length = 0;
        this.accountStore.accounts.push(...accs);
        return this.accountStore.accounts;
      } catch(e) {
        console.log(e);
      }
    } else if (response.status === 401) {
      this.userStore.logOutUser();
      throw new Error('Unauthorized');
    }
    return [];
  }
}