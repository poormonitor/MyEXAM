<script setup>
import { ref, reactive, computed, inject } from 'vue';
import { GetYearMonth, getOptions } from '../func.js';
import { courses, grades, file_types } from '../const';
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

const gotoFile = (eid, pid, fid) => {
	uni.navigateTo({
		url: '/pages/exam/exam?eid=' + eid + '&pid=' + pid + '&fid=' + fid
	});
};

const openDialog = () => {
	popup.value.open();
};

const goSearch = () => {
	loading.value = true;
	uni.request({
		url: 'https://exam.techo.cool/api/search/file',
		data: {
			s: s.value,
			start: searchInfo.range[0],
			end: searchInfo.range[1],
			courses: searchInfo.courses,
			grade: searchInfo.grade ? searchInfo.grade : null,
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

const getHighLight = (text) => {
	return text
		.replaceAll('*s*', `<span class="text-bold text-red">`)
		.replaceAll('*e*', '</span>');
};

if (s.value) goSearch();
defineExpose({ query: goSearch });
</script>

<template>
	<view class="mb-4 mx-20 flex">
		<uni-search-bar
			placeholder="搜索文件"
			v-model="s"
			class="flex-1"
			cancelButton="none"
			bgColor="#ffffff"
			@confirm="goSearch"
		></uni-search-bar>
		<button size="mini" class="mx-2 my-12" type="info" @click="openDialog">
			筛选
		</button>
		<button size="mini" class="mx-0 my-12" type="info" @click="goSearch">
			搜索
		</button>
	</view>
	<uni-popup
		ref="popup"
		background-color="#fff"
		type="right"
		@maskClick="goSearch"
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
		<view class="mx-20 mb-10">找到了 {{ cnt }} 份文件。</view>
		<view v-for="item in data">
			<uni-card
				@click="gotoFile(item.exam.eid, item.paper.pid, item.fid)"
			>
				<view class="flex justify-between">
					<view>
						<view class="flex gap-10">
							<text class="text-red">{{ item.union.name }}</text>
							<text class="text-black">
								{{ GetYearMonth(item.examgroup.date) }}
								{{ item.examgroup.name }}
							</text>
						</view>
						<view class="flex gap-10 mb-6">
							<text>{{ item.exam.date }}</text>
							<text>{{ item.paper.owner }}</text>
							<text>{{ item.paper.comment }}</text>
						</view>
					</view>
					<view class="text-right text-bold">
						<view class="flex gap-5">
							<text>{{ grades[item.exam.grade] }}</text>
							<text>{{ courses[item.exam.course] }}</text>
						</view>
						<view class="text-black text-base">
							{{ file_types[item.type] }}
						</view>
					</view>
				</view>
				<view class="text-bold text-lg text-black mb-2">
					{{ item.name }}
				</view>
				<view
					v-html="getHighLight(t)"
					v-for="t in item.text.slice(0, 2)"
				></view>
			</uni-card>
		</view>
		<view class="mx-30">
			<uni-pagination :total="cnt" v-model="page" @change="goSearch" />
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
