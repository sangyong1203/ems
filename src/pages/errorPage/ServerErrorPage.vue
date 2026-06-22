<template>
    <div class="layout-page">
        <div class="middle">
            <div class="middle-right">
                <div class="middle-right-content">
                    <div class="page-image">
                        <div style="font-size: 50px; font-weight: 700">Server Error</div>
                    </div>
                    <div class="page-description">
                        <p>The server encountered an unexpected error.</p>
                        <p>Please try again later or contact the administrator.</p>
                    </div>

                    <div class="page-button">
                        <el-button type="primary" class="page-btn" @click="goHome">Go to Home</el-button>
                        <el-button
                            class="page-btn"
                            style="border: 1px solid #dedede; margin: 0; background: #f4f4f4"
                            @click="goBack"
                            >Go Back</el-button
                        >
                    </div>

                    <div class="page-footer">If the problem persists, please contact the administrator.</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { useNavStore } from '@/stores/nav.store'

const router = useRouter()
const authStore = useAuthStore()

const goBack = () => {
    router.back()
}

const goHome = () => {
    if (authStore.authState.user?.landingPage) {
        useNavStore().navTo('landingPage', authStore.authState.user.landingPage)
    } else {
        router.push({ name: 'login' })
    }
}
</script>

<style lang="scss" scoped>
.layout-page {
    height: 100%;
    width: 100%;
    background-color: white;
}

.middle {
    display: flex;
    height: 100%;
    width: 100%;
    background-color: white;

    .middle-right {
        width: auto;
        padding: 2.5%;
        display: flex;
        align-items: center;
        flex-direction: column;
        justify-content: center;
        flex: 1;
        height: 100%;

        .middle-right-content {
            gap: 24px;
            display: flex;
            flex-direction: column;
            color: #000000;

            .page-image {
                width: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 20px 0;
            }
            .page-description {
                font-size: 18px;
                font-weight: 400;
                text-align: center;
                line-height: 150%;
                color: #000000;
            }
            .page-button {
                margin-top: 10px;
                display: flex;
                justify-content: center;
                gap: 4px;
                .page-btn {
                    width: 128px !important;
                    height: 44px !important;
                    font-size: 17px;
                }
            }
            .page-footer {
                font-size: 15px;
                font-weight: 400;
                text-align: center;
                color: #666666;
            }
        }
    }
}
</style>
