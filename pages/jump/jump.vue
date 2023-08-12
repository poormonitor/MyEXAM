<script setup>
import { onLoad } from '@dcloudio/uni-app';
import { urlToToObj } from '../../func';

uni.showLoading({ title: '跳转中' });
onLoad((options) => {
	//#ifdef MP-WEIXIN
	options = urlToToObj(decodeURIComponent(options.scene));
	//#endif
	if (options.id) {
		uni.request({
			url: 'https://exam.techo.cool/api/jump/go',
			data: { id: options.id },
			success: (response) => {
				if (response.data.id) {
					let t = response.data.type;
					let idn = response.data.idn;
					let ide = response.data.id;
					uni.hideLoading();
					uni.redirectTo({
						url: `/pages/${t}/${t}?${idn}=${ide}`
					});
				} else {
					uni.hideLoading();
					uni.switchTab({
						url: '/pages/index/index'
					});
				}
			},
			fail: () => {
				uni.hideLoading();
				uni.switchTab({
					url: '/pages/index/index'
				});
			}
		});
	} else {
		uni.hideLoading();
		uni.switchTab({
			url: '/pages/index/index'
		});
	}
});
</script>

<template></template>
