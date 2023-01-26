<script setup>
import { Cart as CartIcon } from "@vicons/ionicons5";

const showCart = ref(false);
</script>
<template>
    <Cart v-model:show="showCart" />
    <div class="fixed right-4 md:right-6 lg:right-8 bottom-16 z-10">
        <n-button
            circle
            secondary
            @click="showCart = true"
            size="large"
            type="info"
        >
            <template #icon>
                <n-icon><CartIcon /></n-icon>
            </template>
        </n-button>
    </div>
    <n-layout class="min-h-full pb-12">
        <n-layout-header bordered>
            <Header></Header>
        </n-layout-header>
        <n-layout-content>
            <router-view></router-view>
        </n-layout-content>
        <n-layout-footer bordered position="absolute">
            <Footer></Footer>
        </n-layout-footer>
    </n-layout>
</template>
