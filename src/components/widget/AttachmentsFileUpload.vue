<template>
    <div class="attachments">
        <el-upload
            ref="uploadRef"
            v-model:file-list="fileList"
            drag
            :action="uploadPath"
            :http-request="uplaodFileData"
            :auto-upload="false"
            :show-file-list="false"
            multiple
            :before-upload="beforeUpload"
            :before-remove="beforeRemove"
            :on-exceed="handleExceed"
            :on-success="uploadSuccess"
            style="width: 50%"
        >
            <div class="place-holder">
                <svg width="30" height="30" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                        d="M10.8333 32.5C8.53 32.5 6.56528 31.701 4.93917 30.1029C3.31306 28.5049 2.5 26.5518 2.5 24.2438C2.5 22.1732 3.16611 20.3521 4.49833 18.7804C5.83056 17.2088 7.48278 16.2776 9.455 15.9871C9.98917 13.4957 11.2419 11.4583 13.2133 9.875C15.1844 8.29167 17.4467 7.5 20 7.5C23.0178 7.5 25.5778 8.55111 27.68 10.6533C29.7822 12.7556 30.8333 15.3156 30.8333 18.3333V19.1667H31.3463C33.1026 19.3033 34.5674 20.0096 35.7404 21.2854C36.9135 22.561 37.5 24.0769 37.5 25.8333C37.5 27.6922 36.859 29.2681 35.5771 30.5608C34.2949 31.8536 32.7243 32.5 30.8654 32.5H21.7629C20.921 32.5 20.2083 32.2083 19.625 31.625C19.0417 31.0417 18.75 30.329 18.75 29.4871V20.3587L15.6667 23.3908L13.9104 21.6508L20 15.5608L26.0896 21.6508L24.3333 23.3908L21.25 20.3587V29.4871C21.25 29.6154 21.3035 29.7329 21.4104 29.8396C21.5171 29.9465 21.6346 30 21.7629 30H30.8333C32 30 32.9861 29.5972 33.7917 28.7917C34.5972 27.9861 35 27 35 25.8333C35 24.6667 34.5972 23.6806 33.7917 22.875C32.9861 22.0694 32 21.6667 30.8333 21.6667H28.3333V18.3333C28.3333 16.0278 27.5208 14.0625 25.8958 12.4375C24.2708 10.8125 22.3056 10 20 10C17.6944 10 15.7292 10.8125 14.1042 12.4375C12.4792 14.0625 11.6667 16.0278 11.6667 18.3333H10.8013C9.22208 18.3333 7.86042 18.9028 6.71625 20.0417C5.57208 21.1806 5 22.5556 5 24.1667C5 25.7778 5.56944 27.1528 6.70833 28.2917C7.84722 29.4306 9.22222 30 10.8333 30H15V32.5H10.8333Z"
                        fill="currentColor"
                    />
                </svg>

                <div class="el-upload__text">
                    Drop file here or
                    <em style="text-decoration: underline; color: var(--secondary-color); font-weight: 500"
                        >click to upload.</em
                    >
                </div>
            </div>
        </el-upload>
        <div class="file-list">
            <div v-for="file in fileList" :key="file.name" class="file-item">
                {{ file.name }}
                <svg
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                    @click="uploadRef?.handleRemove(file)"
                >
                    <path
                        d="M8.4 16.6538L12 13.0538L15.6 16.6538L16.6538 15.6L13.0538 12L16.6538 8.4L15.6 7.34625L12 10.9462L8.4 7.34625L7.34625 8.4L10.9462 12L7.34625 15.6L8.4 16.6538ZM12.0017 21.5C10.6877 21.5 9.45267 21.2507 8.2965 20.752C7.14033 20.2533 6.13467 19.5766 5.2795 18.7218C4.42433 17.8669 3.74725 16.8617 3.24825 15.706C2.74942 14.5503 2.5 13.3156 2.5 12.0017C2.5 10.6877 2.74933 9.45267 3.248 8.2965C3.74667 7.14033 4.42342 6.13467 5.27825 5.2795C6.13308 4.42433 7.13833 3.74725 8.294 3.24825C9.44967 2.74942 10.6844 2.5 11.9983 2.5C13.3123 2.5 14.5473 2.74933 15.7035 3.248C16.8597 3.74667 17.8653 4.42342 18.7205 5.27825C19.5757 6.13308 20.2528 7.13833 20.7518 8.294C21.2506 9.44967 21.5 10.6844 21.5 11.9983C21.5 13.3123 21.2507 14.5473 20.752 15.7035C20.2533 16.8597 19.5766 17.8653 18.7218 18.7205C17.8669 19.5757 16.8617 20.2528 15.706 20.7518C14.5503 21.2506 13.3156 21.5 12.0017 21.5Z"
                        fill="currentColor"
                    />
                </svg>
            </div>
            <p class="file-count">{{ fileList ? fileList.length : 0 }} / 10</p>
        </div>
    </div>
</template>

<script lang="ts" setup>
import type { UploadProps, UploadUserFile } from 'element-plus'
import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth.store'
import { ElLoading } from 'element-plus'

const emits = defineEmits(['uploadDone'])

type Props = {
    path: string
}
const props = defineProps<Props>()

const uploadRef = ref()
const uploadPath = '/system/files'
const fileList = ref<UploadUserFile[]>()


const uplaodFileData = (options: any) => {
    const file = options.file
    const formData = new FormData()
    formData.append('file', file)
    formData.append('storageType', 'EXTERNAL_NFS')
    formData.append('originalName', file.name)
    formData.append('path', props.path)

    return axios
        .post(options.action, formData, {
            headers: {
                Authorization: `Bearer ${useAuthStore().authState.tokens.accessToken}`,
                'Content-Type': 'multipart/form-data',
            },
        })
        .then(response => {
            options.onSuccess(response.data)
        })
        .catch(error => {
            options.onError(error)
        })
}

const handleExceed: UploadProps['onExceed'] = (files, uploadFiles) => {
    ElMessage.warning(
        `The limit is 10, you selected ${files.length} files this time, add up to ${
            files.length + uploadFiles.length
        } totally`,
    )
}
const beforeUpload = (file: any) => {
    const isLt2M = file.size / 1024 / 1024 < 2

    if (!isLt2M) {
        console.error('?뚯씪 ?ш린??2MB瑜?珥덇낵?????놁뒿?덈떎')
    }

    return isLt2M
}
const beforeRemove: UploadProps['beforeRemove'] = (uploadFile, uploadFiles) => {
    return ElMessageBox.confirm(`Cancel the transfer of ${uploadFile.name} ?`, 'Confirm').then(
        () => true,
        () => false,
    )
}


const getRawFiles = () => {
    return fileList.value?.map(el => el.raw)
}

let uploadedFilesCount = 0
const fileIdList = ref<number[]>([])


const uploadSuccess = (res: any) => {
    if (res != null) {
        console.log('upload res', res)
        uploadedFilesCount++
        console.log('uploadedFilesCount : ', uploadedFilesCount)
        fileIdList.value.push(res.data.fileId)
        uploadCompleted()
    }
}


const uploadCompleted = () => {
    if (uploadedFilesCount > 0 && uploadedFilesCount === fileList.value?.length) {

        setTimeout(() => {
            emits('uploadDone', fileIdList.value)
            loadingInstance?.close()
        }, 3000)
    }
}

let loadingInstance: any = null
const fileUPload = () => {
    uploadRef.value?.submit()
    loadingInstance = ElLoading.service({
        lock: true,
        text: 'Saving ...',
        background: 'rgba(75, 75, 75, 0.12)',
    })
}

defineExpose({ getRawFiles, fileUPload })
</script>

<style lang="scss" scoped>
.attachments {
    display: flex;
    flex-direction: row;
    gap: 3%;
    width: 100%;

    .place-holder {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 2%;

        margin-top: 5%;
        margin-bottom: 5%;
        color: var(--primary-color);
    }

    .file-list {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        position: relative;
        width: 50%;

        background-color: var(--surface-muted-color);
        border: 1px solid var(--common-component-border-color);
        color: var(--text-color--body);

        padding: 1%;

        .file-item {
            display: flex;
            align-items: center;
            margin-right: 10px;
            gap: 10px;
            height: 30px;
            padding: 1%;

            background-color: var(--common-control-bg-color);
            border: 1px solid var(--common-control-border-color);
            border-radius: 6px;

            svg {
                color: var(--text-color--muted);
                cursor: pointer;
            }
        }

        .file-count {
            position: absolute;
            top: 0%;
            right: 2%;
        }
    }

    :deep(.el-upload-dragger) {
        padding: 0;
        background-color: rgba(231, 109, 255, 0.08);
        border-color: var(--common-control-border-color);
    }
}
</style>
