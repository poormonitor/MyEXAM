<script setup>
const props = defineProps(["label"]);
</script>

<template>
    <div>
        <span class="text-sm sm:text-base text-zinc-500">
            {{ props.label }}
        </span>
        <div class="text-base sm:text-lg">
            <slot></slot>
        </div>
    </div>
</template>
