<script setup>
import Card from "./Card.vue";
</script>

<template>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-x-2 gap-y-4">
        <Card title="一站式">
            <template #content>
                MyEXAM
                是一个一站式试卷分享平台。用户上传所有的试卷都可以在我们的网站上找到。
            </template>
        </Card>
        <Card title="免登录">
            <template #content>
                和其他的竞品不同，MyEXAM 不需要注册和登录即可下载，免去下载 App
                的烦恼。
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
