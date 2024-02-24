<script setup>
const props = defineProps(["value", "cnt"]);
const emits = defineEmits(["update:value", "finish"]);
const inputRef = ref(null);
const data = ref([]);

const onInput = (index, event) => {
    data.value[index] = event.data?.replace(/[^\d]/g, "").substring(0, 1);

    if (index < inputRef.value.length - 1 && event.data)
        inputRef.value[index + 1].focus();

    emits("update:value", data.value.join(""));

    if (index === inputRef.value.length - 1 && event.data) emits("finish");
};

const goMove = (index, event) => {
    let mp = {
        8: (index) => {
            if (index > 0) inputRef.value[index - 1].focus();
        },
        37: (index) => {
            if (index > 0) inputRef.value[index - 1].focus();
        },
        39: (index) => {
            if (index < inputRef.value.length - 1)
                inputRef.value[index + 1].focus();
        },
    };

    if (event.keyCode in mp) mp[event.keyCode](index);
};
</script>

<template>
    <div class="flex justify-center gap-x-1 md:gap-x-4">
        <input
            ref="inputRef"
            class="w-10 h-10 md:w-14 md:h-14 block text-center text-2xl md:text-4xl font-bold text-gray-700 bg-white bg-clip-padding focus:ring focus:ring-red-400 border-2 border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-red-600 focus:outline-none"
            :maxlength="1"
            @input="(e) => onInput(i - 1, e)"
            @keyup="(e) => goMove(i - 1, e)"
            v-for="i in props.cnt"
        />
    </div>
</template>
