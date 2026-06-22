<template>
    <!-- <FullscreenProgress/> -->

    <el-config-provider :locale="en">
        <RouterView />
    </el-config-provider>
</template>

<script setup lang="ts">
// import {FullscreenProgress } from '@/shared/components'
import { RouterView } from 'vue-router'
import { ElConfigProvider } from 'element-plus'
import en from 'element-plus/es/locale/lang/en'
</script>
