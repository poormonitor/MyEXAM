<script setup>
import { useRouter } from "vue-router";

const props = defineProps(["show"]);
const emits = defineEmits(["update:show"]);
const jid = ref(null);
const axios = inject("axios");
const router = useRouter();
const visible = computed({
    set(val) {
        emits("update:show", val);
    },
    get() {
        return props.show;
    },
});

const goJump = () => {
    axios.get("/jump/go", { params: { id: jid.value } }).then((response) => {
        if (response.data) {
            let params = {};
            params[response.data.idn] = response.data.id;
            router.push({ name: response.data.type, params });
            visible.value = false;
        }
    });
};
</script>

<template>
    <n-modal class="!w-[36rem]" v-model:show="visible">
        <n-card
            title="跳转分享"
            :bordered="false"
            size="huge"
            role="dialog"
            aria-modal="true"
        >
            <div class="mb-4">
                <p class="text-center text-lg md:text-2xl mb-3 md:mb-6">
                    输入6位分享码
                </p>
                <DigitInput :cnt="6" v-model:value="jid" @finish="goJump" />
            </div>
        </n-card>
    </n-modal>
</template>
