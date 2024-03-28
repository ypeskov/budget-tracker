<script setup>
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const props = defineProps(['transaction', 'accounts', 'accountType']);
const emit = defineEmits(['accountChanged']);

const t = useI18n().t;

function changeAccount($event) {
  const acc = props.accounts[$event.target.value];
  emit('accountChanged', {
    accountType: props.accountType,
    accountId: acc.id,
  });
}

const accountIdx = computed(() => {
  if (props.accountType === 'src') {
    return props.accounts.findIndex((item) => item.id === props.transaction.accountId);
  } else {
    return props.accounts.findIndex((item) => item.id === props.transaction.targetAccountId);
  }
});

const accLabel = computed(() => {
  if (props.accountType === 'src') {
    return t('message.account');
  } else {
    return t('message.targetAccount');
  }
});
</script>

<template>
  <label for="label" class="form-label">
    {{ accLabel }}
  </label>
  <select class="form-select bottom-space" @change="changeAccount" :value="accountIdx">
    <option v-for="(acc, index) in accounts" :key="acc.id" :value="index">
      {{ acc.name }} ({{ acc.balance }} {{ acc.currency.code }})
    </option>
  </select>
</template>
