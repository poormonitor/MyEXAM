<script setup>
import { message } from "../discrete";
const axios = inject("axios");

const CleanAction = () => {
    axios.post("/system/clean").then((response) => {
        if (response.data.result === "success") {
            message.success("清理成功。");
        }
    });
};

const CleanIsolateAction = () => {
    axios.post("/system/isolate").then((response) => {
        if (response.data.result === "success") {
            message.success("清理成功。");
        }
    });
};

const UpgradeAction = () => {
    axios.post("/system/upgrade").then((response) => {
        if (response.data.result === "success") {
            message.success("更新请求成功。");
        }
    });
};
</script>

<template>
    <p class="text-3xl font-bold pb-8 pt-2">系统管理</p>
    <div class="flex flex-col gap-y-8">
        <n-card title="清理未完成试卷">
            清理系统中用户创建但没有完成上传的试卷。
            <template #action>
                <div class="flex justify-end">
                    <n-button type="primary" @click="CleanAction">
                        清理
                    </n-button>
                </div>
            </template>
        </n-card>
        <n-card title="清理孤立项目">
            清理系统中孤立的项目，包括考试、试卷和文件。
            <template #action>
                <div class="flex justify-end">
                    <n-button type="primary" @click="CleanIsolateAction">
                        清理
                    </n-button>
                </div>
            </template>
        </n-card>
        <n-card title="更新系统">
            更新MyExam程序文件，并重新构建前端应用。后端需要手动重启。
            <template #action>
                <div class="flex justify-end">
                    <n-button type="primary" @click="UpgradeAction">
                        更新
                    </n-button>
                </div>
            </template>
        </n-card>
    </div>
</template>
