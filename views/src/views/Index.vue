<script setup>
import { Cart as CartIcon, ArrowRedo } from "@vicons/ionicons5";

const showCart = ref(false);
const showShare = ref(false);
</script>
<template>
    <Cart v-model:show="showCart" />
    <GoShare v-model:show="showShare" />
    <div class="fixed right-4 md:right-6 lg:right-8 bottom-28 z-10">
        <n-button
            circle
            secondary
            @click="showShare = true"
            size="large"
            type="success"
        >
            <template #icon>
                <n-icon><ArrowRedo /></n-icon>
            </template>
        </n-button>
    </div>
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
            <router-view v-slot="{ Component }">
                <keep-alive>
                    <component :is="Component" />
                </keep-alive>
            </router-view>
        </n-layout-content>
        <n-layout-footer bordered position="absolute">
            <Footer></Footer>
        </n-layout-footer>
    </n-layout>
</template>
