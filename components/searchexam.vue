<script setup>
import { ref, reactive, computed, inject } from 'vue';
import { GetYearMonth, getOptions } from '../func.js';
import { courses, grades } from '../const';
import empty from './empty.vue';

const props = defineProps(['s']);
const emits = defineEmits(['update:s']);
const popup = ref(null);
const s = inject('s');
const loading = inject('loading');

const searchInfo = reactive({
	range: [Date.now() - 1000 * 60 * 60 * 24 * 240, Date.now()],
	grade: null,
	courses: []
});
const data = ref(null);
const cnt = ref(0);
const page = ref(1);

const gotoExam = (eid) => {
	uni.navigateTo({
		url: '/pages/exam/exam?eid=' + eid
	});
};

const openDialog = () => {
	popup.value.open();
};

const reSearch = () => {
	page.value = 1;
	cnt.value = 0;
	goSearch();
};

const goSearch = () => {
	loading.value = true;
	uni.request({
		url: 'https://exam.techo.cool/api/search/exam',
		data: {
			name: s.value,
			start: searchInfo.range[0],
			end: searchInfo.range[1],
			courses: searchInfo.courses,
			grade: searchInfo.grade >= 0 ? searchInfo.grade : null,
			page: page.value
		},
		method: 'POST',
		success: (response) => {
			if (response.data.list) {
				data.value = response.data.list;
				cnt.value = response.data.count;
				loading.value = false;
			}
		}
	});
};

if (s.value) goSearch();
defineExpose({ query: goSearch });
</script>

<template>
	<view class="mb-4 mx-20 flex">
		<uni-search-bar
			placeholder="搜索试卷"
			v-model="s"
			class="flex-1"
			cancelButton="none"
			bgColor="#ffffff"
			@confirm="goSearch"
		></uni-search-bar>
		<button size="mini" class="mx-2 my-12" type="info" @click="openDialog">
			筛选
		</button>
		<button size="mini" class="mx-2 my-12" type="info" @click="reSearch">
			搜索
		</button>
	</view>
	<uni-popup
		ref="popup"
		background-color="#fff"
		type="right"
		@maskClick="reSearch"
	>
		<view class="text-xl text-bold mx-30 mt-30 mb-10">筛选考试</view>
		<view class="filter-popup">
			<uni-section title="考试时间" class="mb-10" type="line">
				<view class="flex items-center mb-8">
					<view class="mr-10">从</view>
					<uni-datetime-picker
						v-model="searchInfo.range[0]"
						type="date"
						:clear-icon="false"
						return-type="timestamp"
					/>
				</view>
				<view class="flex items-center">
					<view class="mr-10">到</view>
					<uni-datetime-picker
						v-model="searchInfo.range[1]"
						type="date"
						:clear-icon="false"
						return-type="timestamp"
					/>
				</view>
			</uni-section>
			<uni-section title="考试年级" class="mb-10" type="line">
				<uni-data-select
					v-model="searchInfo.grade"
					:localdata="getOptions(grades)"
				></uni-data-select>
			</uni-section>
			<uni-section title="考试科目" class="mb-10" type="line">
				<uni-data-checkbox
					v-model="searchInfo.courses"
					:multiple="true"
					:localdata="getOptions(courses)"
				></uni-data-checkbox>
			</uni-section>
		</view>
	</uni-popup>
	<view v-if="data">
		<view class="mx-20 mb-10">找到了 {{ cnt }} 场考试。</view>
		<view v-for="item in data">
			<uni-card @click="gotoExam(item.eid)">
				<view class="flex justify-between mb-4">
					<view>
						<view class="text-bold text-red mb-2">
							{{ item.union.name }}
						</view>
						<view class="text-bold text-lg text-black">
							{{ GetYearMonth(item.examgroup.date) }}
							{{ item.examgroup.name }}
						</view>
					</view>
					<view class="text-right">
						<view class="mb-2">{{ item.date }}</view>
						<view class="text-black text-bold text-lg">
							{{ grades[item.grade] }} {{ courses[item.course] }}
						</view>
					</view>
				</view>
			</uni-card>
		</view>
		<view class="mx-30 py-10">
			<uni-pagination
				show-icon="true"
				:total="cnt"
				v-model="page"
				@change="goSearch"
			/>
		</view>
	</view>
	<empty v-else />
</template>

<style>
.filter-popup {
	width: 200px;
	margin: 0 2rem;
}
</style>
