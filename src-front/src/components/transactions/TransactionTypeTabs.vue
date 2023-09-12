<script setup>
import { ref } from 'vue';

const props = defineProps(['transaction']);
const currentItem = ref('expense');

function changeItemType($event) {
  currentItem.value = $event.target.getAttribute('data-itemtype');
}
</script>

<template>
  <ul @click="changeItemType" class="nav nav-pills bottom-space top-space">
    <li class="nav-item">
      <a
        id="expense-item"
        data-qwer="1111"
        data-rrr="777"
        class="nav-link"
        :class="{ active: currentItem === 'expense' }"
        data-itemtype="expense"
        href="#">
        Active
      </a>
    </li>
    <li class="nav-item">
      <a
        id="income-item"
        class="nav-link"
        :class="{ active: currentItem === 'income' }"
        data-itemtype="income"
        href="#">
        Link
      </a>
    </li>
    <li class="nav-item">
      <a
        id="transfer-item"
        class="nav-link"
        :class="currentItem == 'transfer' ? 'active' : ''"
        data-itemtype="transfer"
        href="#">
        Link
      </a>
    </li>
  </ul>
</template>
