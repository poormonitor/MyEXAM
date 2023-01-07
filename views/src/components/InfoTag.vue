<script setup>
const props = defineProps(["label"])
</script>

<template>
    <div>
        <span class="text-zinc-500">{{ props.label }}</span>
        <div class="text-lg">
            <slot></slot>
        </div>
    </div>
</template>