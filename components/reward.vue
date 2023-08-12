<script setup>
import { inject, ref } from 'vue';
import { onShow } from '@dcloudio/uni-app';

const alertDialog = ref(null);
const confirmDialog = ref(null);
const title = ref('');
const content = ref('');
const action = ref(() => {});
const lefts = inject('lefts');
const adUnitId = inject('reward');

var loaded = false;
var AdObject = null;

const onadclose = (e) => {
	const detail = e.detail;
	if (detail && detail.isEnded) {
		lefts.reset();
		lefts.reduce();
		emits('confirm');
	} else {
		alertDialog.value.open();
	}
};

const onadload = (e) => {
	console.log(e.detail);
	loaded = true;
};

const onaderror = (e) => {
	console.log(e.detail);
};

const query = (callback) => {
	if (!loaded) return callback();
	if (lefts.length()) {
		title.value = '扣除下载次数';
		content.value = `当前剩余 ${lefts.length()} 次下载, 确认扣除？`;
		action.value = () => {
			callback();
			lefts.reduce();
		};
		confirmDialog.value.open();
	} else {
		title.value = '下载次数不足';
		content.value = '当前下载次数不足, 观看广告以获得 5 次下载';
		action.value = () => {
			console.log(AdObject);
			AdObject.show();
		};
		confirmDialog.value.open();
	}
};

onShow(() => {
	if (wx.createRewardedVideoAd && adUnitId) {
		AdObject = wx.createRewardedVideoAd({ adUnitId });
		AdObject.onLoad(onadload);
		AdObject.onError(onaderror);
		AdObject.onclose(onadclose);
	}
});

defineExpose({ query });
</script>

<template>
	<uni-popup ref="alertDialog" type="message">
		<uni-popup-message
			type="error"
			message="没有完整播放哦"
			:duration="2000"
		></uni-popup-message>
	</uni-popup>
	<uni-popup ref="confirmDialog" type="dialog">
		<uni-popup-dialog
			type="warn"
			cancelText="取消"
			confirmText="好的"
			:title="title"
			:content="content"
			@confirm="action"
		></uni-popup-dialog>
	</uni-popup>
</template>
