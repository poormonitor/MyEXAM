<script setup>
import CartList from "./CartList.vue";
</script>

<template>
    <n-modal class="!m-4 md:!mx-auto md:!w-[80vw]">
        <n-card
            title="收藏夹"
            :bordered="false"
            size="huge"
            role="dialog"
            aria-modal="true"
        >
            <CartList />
        </n-card>
    </n-modal>
</template>
