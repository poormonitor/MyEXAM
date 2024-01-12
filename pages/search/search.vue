<script setup>
import { ref, inject, computed } from 'vue';
import searchexam from '../../components/searchexam.vue';
import searchfile from '../../components/searchfile.vue';
import { onShow } from '@dcloudio/uni-app';

const props = defineProps(['t', 's']);
const current = ref(props.t ? props.t : 0);
const items = ['搜索考试', '搜索文件'];
const last = ref('');
const s = inject('s');
const resultRef1 = ref(null);
const resultRef2 = ref(null);

const onClickItem = (e) => {
	if (current.value != e.currentIndex) {
		current.value = e.currentIndex;
	}
};

const item = computed(() => {
	if (current.value === 0) return resultRef1.value;
	if (current.value === 1) return resultRef2.value;
});

onShow(() => {
	if (last.value != s.value && item.value) item.value.query();
	last.value = s.value;
});
</script>

<template>
	<view>
		<view class="mx-30 mt-20 mb-10">
			<uni-segmented-control
				@clickItem="onClickItem"
				:current="current"
				:values="items"
				activeColor="#7f0f1d"
			/>
		</view>
		<view class="content pb-10">
			<searchexam v-if="current === 0" ref="resultRef1"></searchexam>
			<searchfile v-if="current === 1" ref="resultRef2"></searchfile>
		</view>
	</view>
</template>
