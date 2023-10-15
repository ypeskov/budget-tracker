<script setup>
import { onBeforeMount, reactive } from 'vue';
import { useRouter } from 'vue-router';

import { useUserStore } from '../../stores/user';
import { useAccountStore } from '../../stores/account';
import { AccountService } from '../../services/accounts';

const router = useRouter();
const userStore = useUserStore();
const accountStore = useAccountStore();
const accountService = new AccountService(userStore, accountStore);

const accounts = reactive([]);

onBeforeMount(async () => {
  try {
    accounts.length = 0;
    accounts.push(...(await accountService.getAllUserAccounts()));
    console.log(accounts);
  } catch (e) {
    console.log(e.message);
    router.push({ name: 'login' });
  }
});

</script>

<template>
  <div class="row">
    <div class="col">
      <div class="list-item account-item" v-for="acc in accounts" :key="acc.id">
        <span class="acc-name">
          <input class="form-check-input" type="checkbox" value="" id="" />
          <label class="form-check-label" for="form-check-input">{{  acc.name }}</label>
        </span>
        <span>( {{ acc.currency.code }} {{ acc.balance }} )</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.account-item {
  display: flex;
  justify-content: space-between;
}
.form-check-input {
  margin-right: 1vw;
}
</style>