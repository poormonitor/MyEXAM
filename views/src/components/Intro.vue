<script setup>
import Card from "./Card.vue";
</script>

<template>
    <div
        class="mx-4 md:mx-auto md:w-[90vw] lg:w-[80vw] grid grid-cols-1 md:grid-cols-3 gap-x-2 gap-y-4"
    >
        <Card title="一站式">
            <template #content>
                MyEXAM
                是一个一站式试卷分享平台。所有的试卷都可以在我们的网站上找到。
            </template>
        </Card>
        <Card title="免登录">
            <template #content>
                和其他的竞品不同，MyEXAM
                不需要登陆即可上传和下载，让用户无障碍使用。
            </template>
        </Card>
        <Card title="共享化">
            <template #content>
                通过用户上传，MyEXAM
                实现了学习资源的最大化共享，帮助所有用户提升自我。
            </template>
        </Card>
    </div>
</template>
