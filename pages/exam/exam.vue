<script setup>
import { ref, inject, provide } from 'vue';
import { GetYearMonth } from '../../func';
import { courses, grades } from '../../const';
import reward from '../../components/reward.vue';
import filelist from '../../components/filelist.vue';

const props = defineProps(['eid', 'pid', 'fid']);
const rewardRef = ref(null);
const data = ref(null);
const carts = inject('carts');
const loading = inject('loading');

const gotoUnion = (nid) => {
	uni.navigateTo({
		url: '/pages/union/union?nid=' + nid
	});
};

const gotoExamGroup = (egid) => {
	uni.navigateTo({
		url: '/pages/examgroup/examgroup?egid=' + egid
	});
};

if (props.eid) {
	loading.value = true;
	uni.request({
		url: 'https://exam.techo.cool/api/list/exam',
		data: { eid: props.eid },
		success: (response) => {
			if (response.data.exam) data.value = response.data.exam;
			if (props.pid && !props.fid) {
				uni.pageScrollTo({
					selector: '#' + props.pid
				});
			}
			loading.value = false;
		}
	});
} else {
	uni.switchTab({
		url: '/pages/index/index'
	});
}

provide('rewardRef', rewardRef);
</script>

<template>
	<view class="p-30" v-if="data">
		<reward ref="rewardRef" />
		<view id="title" class="mb-15">
			<view
				class="mb-3 flex items-start"
				@click="gotoUnion(data.union.nid)"
			>
				<view class="text-xl text-red">{{ data.union.name }}</view>
				<image
					src="../../static/icons8-share-24.png"
					style="width: 16px; height: 16px"
					class="ml-4"
					mode="scaleToFill"
				></image>
			</view>
			<view
				class="text-2xl text-bold flex items-start mb-2"
				@click="gotoExamGroup(data.examgroup.egid)"
			>
				{{ GetYearMonth(data.examgroup.date) }}
				{{ data.examgroup.name }}
				<image
					src="../../static/icons8-share-48.png"
					style="width: 20px; height: 20px"
					class="ml-5"
					mode="scaleToFill"
				></image>
			</view>
			<view class="text-lg mb-5">
				{{ grades[data.grade] }} {{ courses[data.course] }}
			</view>
			<view class="mb-2 text-sm">
				<text class="mr-15">{{ data.date }}</text>
				<text>{{ data.views }} 浏览</text>
			</view>
		</view>
		<!--  #ifdef MP -->
		<view class="mb-10">
			<button open-type="share" size="mini" type="info">分享</button>
		</view>
		<!--  #endif -->
		<view class="mt-15">
			<view v-for="paper in data.papers" :id="paper.pid">
				<uni-card
					:class="{ 'highlight-card': paper.pid === props.pid }"
					:title="paper.owner + ' ' + paper.comment"
					:is-full="true"
				>
					<view class="mb-5 flex justify-between items-center">
						<view>
							<text class="mr-10">
								{{ paper.files.length }} 份文件
							</text>
							<text>浏览量：{{ paper.views }}</text>
						</view>
						<view>
							<button
								@click="() => carts.remove(paper.pid)"
								size="mini"
								type="info"
								v-if="carts.has(paper.pid)"
							>
								<span class="whitespace-nowrap">收藏</span>
							</button>
							<button
								@click="() => carts.add(paper.pid)"
								size="mini"
								type="default"
								v-else
							>
								<span class="whitespace-nowrap">收藏</span>
							</button>
						</view>
					</view>
					<view>
						<filelist :files="paper.files" :fid="props.fid" />
					</view>
				</uni-card>
			</view>
		</view>
	</view>
</template>

<style>
.hightlight-card {
	background-color: blue;
}
</style>
