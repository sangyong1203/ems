<template>
    <BaseDialog :model-value="isShowDialog" title="Template preview" width="90%" @on-close="onClose">
        <div class="preview-container">
            <div class="preview-content">
                <div class="notification-preview">
                    <div class="template-content">
                        <div class="email-header" v-if="previewData.title">
                            <h1 class="email-title">{{ previewData.title }}</h1>
                        </div>
                        <div class="email-body" v-if="previewData.body">
                            <div class="body-content" v-html="previewData.body"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <template #footer>
            <el-button type="primary" @click="onClose">OK</el-button>
        </template>
    </BaseDialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { getAuthImage } from '@/services/file.service'


function decodeHTMLEntities(html: string): string {
    const txt = document.createElement('textarea')
    txt.innerHTML = html
    return txt.value
}


function applyPreviewContext(str: string, context: Record<string, string>): string {
    Object.entries(context).forEach(([key, value]) => {
        const reg = new RegExp(`{{\\s*${key}\\s*}}`, 'g')
        str = str.replace(reg, value)
    })
    return str
}

const isShowDialog = ref(false)
const previewData = ref({
    type: '',
    title: '',
    body: '',
    imageSubstitutions: [] as any[],
    inUse: true,
})


const dummyContext = {
    user_name: 'User Name',
    user_id: 'hongildong',
    user_email: 'hongildong@example.com',
}

const openDialog = async (templateData: any, imageSubs: any[]) => {
    console.log('Raw templateData.body:', templateData.body)
    console.log('Image substitutions:', imageSubs)


    let html = decodeHTMLEntities(templateData.body)
    console.log('Decoded body:', html)
    html = applyPreviewContext(html, dummyContext)


    for (const sub of imageSubs) {
        if (sub.urlData) {
            const blobUrl = await getAuthImage(sub.urlData)
            if (blobUrl) {
                sub.blobUrl = blobUrl
            }
        }
    }


    imageSubs.forEach(sub => {
        if (sub.substitution) {

            let cleanSub = sub.substitution.trim().replace(/^\{\{/, '').replace(/\}\}$/, '').trim()
            console.log(`Replacing {{${cleanSub}}} with image:`, sub.blobUrl || sub.urlData)


            const escapedSub = cleanSub.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
            const imagePattern = new RegExp(`{{\\s*${escapedSub}\\s*}}`, 'g')
            const imgTag = `<img src="${sub.blobUrl || sub.urlData}" alt="${sub.imageName}" style="max-width: 100%; height: auto;" />`
            html = html.replace(imagePattern, imgTag)
        }
    })
    console.log('Final body after image replacement:', html)

    previewData.value = {
        ...templateData,
        body: html,
        imageSubstitutions: imageSubs,
    }
    isShowDialog.value = true
}

const onClose = () => {
    isShowDialog.value = false
}
defineExpose({ openDialog })
</script>

<style scoped>
.preview-container {
    padding: 20px;
    background-color: #f5f5f5;
    min-height: 65vh;
    overflow-y: auto;
}
.preview-content {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    height: 100%;
}
.notification-preview {
    background-color: white;
    padding: 40px;
    width: 100%;
    min-height: 100%;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.template-content {
    color: #333;
}
.email-header {
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 2px solid #e4e7ed;
}
.email-title {
    margin: 0;
    font-size: 28px;
    font-weight: 600;
    color: #303133;
}
.email-body {
    margin-top: 20px;
}
.body-content {
    font-size: 15px;
    line-height: 1.8;
    color: #606266;
}
.body-content :deep(p) {
    margin: 0 0 1em 0;
}
.body-content :deep(img) {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1em 0;
}
.body-content :deep(h1),
.body-content :deep(h2),
.body-content :deep(h3),
.body-content :deep(h4),
.body-content :deep(h5),
.body-content :deep(h6) {
    margin: 1em 0 0.5em 0;
    font-weight: 600;
}
.body-content :deep(ul),
.body-content :deep(ol) {
    padding-left: 20px;
    margin: 0.5em 0;
}
.body-content :deep(blockquote) {
    border-left: 4px solid #dcdfe6;
    padding-left: 15px;
    margin: 1em 0;
    color: #909399;
}
</style>
