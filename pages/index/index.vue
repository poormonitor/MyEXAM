<script setup>
import { ref, reactive, inject, watch } from 'vue';
import { GetYearMonth, getOptions, cleanEmpty } from '../../func';
import { courses, grades } from '../../const';
const data = ref([]);
const s = inject('s');
const loading = ref(false);
const SearchInfo = reactive({
	latest: true,
	course: null,
	grade: null
});

const cleanOption = () => {
	SearchInfo.latest = true;
	SearchInfo.course = null;
	SearchInfo.grade = null;
};

const gotoExam = (eid) => {
	uni.navigateTo({
		url: '/pages/exam/exam?eid=' + eid
	});
};

const goSearch = () => {
	if (!s.value) return;
	uni.switchTab({
		url: '/pages/search/search'
	});
};

const requestRecent = () => {
	loading.value = true;
	uni.request({
		url: 'https://exam.techo.cool/api/discover/exams',
		data: cleanEmpty(SearchInfo),
		method: 'POST',
		success: (response) => {
			if (response.data.list) data.value = response.data.list;
			loading.value = false;
		}
	});
};
watch(SearchInfo, requestRecent, { immediate: true });
</script>

<template>
	<view class="p-25" v-if="data">
		<view id="title" class="mt-20 mb-24 title text-bold text-center">
			<view class="text-2xl">试卷分享平台</view>
			<view class="text-3xl">MyEXAM</view>
		</view>
		<view class="mb-30 flex">
			<uni-search-bar
				placeholder="搜索试卷"
				bgColor="#ffffff"
				class="flex-1"
				v-model="s"
				cancelButton="none"
				@confirm="goSearch"
			></uni-search-bar>
			<button
				size="mini"
				class="mx-0 my-12"
				type="info"
				@click="goSearch"
			>
				搜索
			</button>
		</view>
		<view>
			<view class="text-bold text-center mb-16">最近上传</view>
			<view class="flex justify-center">
				<view class="flex gap-10" style="width: 70vw">
					<view style="flex-basis: 50%">
						<uni-data-select
							placeholder="年级"
							v-model="SearchInfo.grade"
							:localdata="getOptions(grades)"
						></uni-data-select>
					</view>
					<view style="flex-basis: 50%">
						<uni-data-select
							placeholder="学科"
							v-model="SearchInfo.course"
							:localdata="getOptions(courses)"
						></uni-data-select>
					</view>
				</view>
			</view>
			<view class="flex flex-col justify-center mt-30" v-if="loading">
				<text class="mb-10 text-center">加载中</text>
			</view>
			<view
				class="flex flex-col justify-center mt-30"
				v-else-if="!data.length"
			>
				<text class="mb-10 text-center">这里什么也没有</text>
				<button size="mini" @click="cleanOption">清空条件</button>
			</view>
			<view v-for="item in data">
				<uni-card @click="gotoExam(item.eid)">
					<view class="flex justify-between mb-4">
						<view class="text-bold text-red">
							{{ item.union.name }}
						</view>
						<view class="text-right">
							<view>{{ item.date }}</view>
						</view>
					</view>
					<view
						class="text-bold text-lg text-black"
						style="line-height: 130%"
					>
						{{ GetYearMonth(item.examgroup.date) }}
						{{ item.examgroup.name }}
					</view>
					<view>
						{{ grades[item.grade] }}
						{{ courses[item.course] }}
					</view>
				</uni-card>
			</view>
		</view>
	</view>
</template>

<style>
.title {
	background-image: linear-gradient(
		to bottom left,
		#f11b3b,
		#ce1733,
		#7f0f1d
	);
	-webkit-background-clip: text;
	background-clip: text;
	color: transparent;
}
</style>
