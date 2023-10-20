<script setup>
import { computed } from 'vue';

const props = defineProps(['itemType']);
const currentItem = computed(() => props.itemType);
const emit = defineEmits(['typeChanged']);

function changeItemType($event) {
  currentItem.value = $event.target.getAttribute('data-itemtype');
  emit('typeChanged', currentItem.value);
}
</script>

<template>
  <ul @click="changeItemType" class="nav nav-pills bottom-space top-space">
    <li class="nav-item">
      <a
        id="expense-item"
        class="nav-link"
        :class="{ active: currentItem === 'expense' }"
        data-itemtype="expense"
        href="#">
        Expense
      </a>
    </li>
    <li class="nav-item">
      <a
        id="income-item"
        class="nav-link"
        :class="{ active: currentItem === 'income' }"
        data-itemtype="income"
        href="#">
        Income
      </a>
    </li>
    <li class="nav-item">
      <a
        id="transfer-item"
        class="nav-link"
        :class="currentItem == 'transfer' ? 'active' : ''"
        data-itemtype="transfer"
        href="#">
        Transfer
      </a>
    </li>
  </ul>
</template>
