<script setup>
import { ArrowRedo } from "@vicons/ionicons5";

const props = defineProps(["type", "id"]);
const axios = inject("axios");
const jid = ref(null);
const code = ref(null);

const handleUpdateShow = () => {
    if (!jid.value)
        axios
            .post("/jump/generate", { type: props.type, id: props.id })
            .then((response) => {
                if (response.data) {
                    jid.value = response.data.jid;
                    code.value =
                        "data:image/jpeg;base64," + response.data.qrcode;
                }
            });
};
</script>

<template>
    <n-popover trigger="click" @update:show="handleUpdateShow">
        <template #trigger>
            <n-button size="small" type="error" secondary>
                <template #icon>
                    <n-icon><ArrowRedo /></n-icon>
                </template>
                分享
            </n-button>
        </template>
        <div class="w-60 h-36">
            <div class="flex justify-between h-full p-4" v-if="jid">
                <div class="flex flex-col place-content-center">
                    <p class="text-lg">分享码</p>
                    <p class="font-mono font-bold text-2xl">{{ jid }}</p>
                </div>
                <div class="flex flex-col place-content-center gap-y-2">
                    <img class="w-24" :src="code" />
                    <p class="text-center">微信小程序</p>
                </div>
            </div>
            <div class="h-full flex justify-center" v-else>
                <n-spin><template #description>加载中</template></n-spin>
            </div>
        </div>
    </n-popover>
</template>
