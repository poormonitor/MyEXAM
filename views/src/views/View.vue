<script setup></script>

<template>
    <div class="mx-8 w-auto lg:mx-auto lg:w-[70vw] pt-8 pb-12">
        <Suspense>
            <router-view />
            <template #fallback>
                <div class="flex place-content-center mt-12">
                    <n-spin>
                        <template #description> 加载中 </template>
                    </n-spin>
                </div>
            </template>
        </Suspense>
    </div>
</template>
