<script setup></script>

<template>
    <div class="mx-8 w-auto lg:mx-auto lg:w-[70vw] pt-8 pb-12">
        <router-view v-slot="{ Component }">
            <Suspense :key="Component">
                <div id="view-content">
                    <component :is="Component" />
                </div>
                <template #fallback>
                    <div class="flex place-content-center mt-[40vh]">
                        <n-spin>
                            <template #description> 加载中 </template>
                        </n-spin>
                    </div>
                </template>
            </Suspense>
        </router-view>
    </div>
</template>
