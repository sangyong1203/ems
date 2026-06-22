<template>
    <div v-if="progressStore.isProgressing" class="progress__overlay">
        <div class="progress__barBox">
            <el-progress
                style="width: 500px"
                :percentage="progressStore.percentCompleted"
                :stroke-width="10"
                striped
                striped-flow
                :duration="10"
            />
            <div style="padding: 10px; margin-left: -20px">
                <span v-if="progressStore.percentCompleted !== 100">
                    Uploading . . .
                </span>
                <span v-if="progressStore.percentCompleted === 100">
                    Upload complete. Waiting for server to finish processing . . .
                </span>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useProgress } from '@/shared/composables/useProgressBar'
const progressStore = useProgress()

</script>

<style lang="scss" scoped>
.progress__overlay {
    width: 100vw;
    height: 100vh;
    position: absolute;
    background-color: #00000080;
    z-index: 5000;
    display: flex;
    justify-content: center;
    align-items: center;
}
.progress__barBox {
    height: 200px;
    color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
}
:deep(.el-progress__text span){
    color: white;
}
</style>
