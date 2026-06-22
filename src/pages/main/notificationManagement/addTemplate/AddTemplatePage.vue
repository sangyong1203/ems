<template>
    <h2 class="title">{{ isEditMode ? 'Edit Template' : 'Add Template' }}</h2>
    <PageBody>
        <ContentBlock className="scrollable-form">
            <div class="form-scroll-area">
                <el-form ref="templateFormRef" :model="templateForm" label-width="180px" label-position="left">
                    <el-form-item label="Type" prop="typeId" required>
                        <el-select
                            v-model="templateForm.typeId"
                            placeholder="Select template type"
                            style="width: 400px"
                        >
                            <el-option
                                v-for="type in availableTypes"
                                :key="type.id"
                                :label="type.type"
                                :value="type.id"
                            />
                        </el-select>
                    </el-form-item>

                    <el-form-item label="Title" prop="title" required>
                        <el-input
                            v-model="templateForm.title"
                            placeholder="Input title"
                            maxlength="255"
                            show-word-limit
                        />
                    </el-form-item>

                    <el-form-item label="Body" prop="body" required>
                        <el-input
                            v-model="templateForm.body"
                            type="textarea"
                            :rows="12"
                            placeholder="Enter the email body content"
                        />
                    </el-form-item>

                    <el-form-item label="Image Substitution">
                        <div class="image-substitution-section">
                            <div class="image-header-row">
                                <el-button class="action-button" @click="openFileDialog">Search</el-button>
                                <input
                                    ref="fileInput"
                                    type="file"
                                    multiple
                                    accept="image/*"
                                    style="display: none"
                                    @change="handleFileChange"
                                />
                                <span class="file-count">{{ selectedLocalFiles.length }} files selected</span>
                            </div>

                            <div v-if="selectedLocalFiles.length" class="selected-files-container">
                                <el-tag
                                    v-for="(file, index) in selectedLocalFiles"
                                    :key="file.name + file.size"
                                    closable
                                    type="info"
                                    @close="removeLocalFile(index)"
                                >
                                    {{ file.name }}
                                </el-tag>
                            </div>
                        </div>
                    </el-form-item>

                    <div class="form-actions">
                        <el-button @click="goBack">Cancel</el-button>
                        <el-button type="primary" :loading="isSaving" @click="saveTemplate">
                            {{ isEditMode ? 'Update' : 'Create' }}
                        </el-button>
                    </div>
                </el-form>
            </div>
        </ContentBlock>
    </PageBody>
</template>

<script lang="ts" setup>
import { computed, onMounted, reactive, ref } from 'vue'
import type { FormInstance } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import { ContentBlock, PageBody } from '@/shared/components'
import { Notification } from '@/shared/composables/useFeedback'
import addTemplateApi from './service/api'
import notificationManagementApi from '../service/notificationManagement.api'
import type { TemplateType } from '../service/notificationManagement.types'

const route = useRoute()
const router = useRouter()

const templateFormRef = ref<FormInstance | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const selectedLocalFiles = ref<File[]>([])
const availableTypes = ref<TemplateType[]>([])
const isSaving = ref(false)

const templateId = computed(() => {
    const id = Number(route.query.id ?? route.params.id)
    return Number.isFinite(id) && id > 0 ? id : null
})
const isEditMode = computed(() => Boolean(templateId.value))

const templateForm = reactive({
    typeId: null as number | null,
    title: '',
    body: '',
})

const openFileDialog = () => {
    fileInput.value?.click()
}

const handleFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement
    selectedLocalFiles.value = Array.from(target.files ?? [])
}

const removeLocalFile = (index: number) => {
    selectedLocalFiles.value.splice(index, 1)
}

const loadTypes = async () => {
    const [typesRes, templatesRes] = await Promise.all([
        notificationManagementApi.getTemplateTypes(),
        notificationManagementApi.getList({
            activeFlag: ['Y', 'N'],
            searchType: '',
            searchKeyword: '',
            pageNumber: 1,
            pageSize: 10,
            sortColumn: '',
            sortDirection: '',
        }),
    ])

    if (typesRes.result !== 'success' || templatesRes.result !== 'success') {
        Notification.error('Failed to load template types.')
        availableTypes.value = []
        return
    }

    const usedTypes = templatesRes.data.list
        .filter(template => !templateId.value || template.id !== templateId.value)
        .map(template => template.type)

    availableTypes.value = typesRes.data.filter(type => !usedTypes.includes(type.type))
}

const loadTemplate = async () => {
    if (!templateId.value) return
    const res = await notificationManagementApi.getTemplate(templateId.value)

    if (res.result !== 'success') {
        Notification.error(res.resultMessage || 'Failed to load template.')
        return
    }

    const template = res.data
    if (!template) return

    const matchedType = availableTypes.value.find(type => type.type === template.type || type.id === template.typeId)
    templateForm.typeId = matchedType?.id ?? template.typeId ?? null
    templateForm.title = template.title ?? ''
    templateForm.body = template.body ?? ''
}

const saveTemplate = async () => {
    if (!templateForm.typeId || !templateForm.title.trim() || !templateForm.body.trim()) {
        Notification.warning('Please fill in required fields.')
        return
    }

    const selectedType = availableTypes.value.find(type => type.id === templateForm.typeId)
    const payload = {
        id: templateId.value ?? 0,
        type: selectedType?.type ?? '',
        title: templateForm.title.trim(),
        body: templateForm.body,
        activeFlag: ['Y'],
        updatedAt: '',
    }

    isSaving.value = true
    try {
        const res = templateId.value
            ? await addTemplateApi.editTemplate(payload, templateId.value)
            : await addTemplateApi.createTemplate(payload)

        if (res.result === 'success') {
            Notification.success('Template saved.')
            goBack()
        } else {
            Notification.error(res.resultMessage || 'Failed to save template.')
        }
    } finally {
        isSaving.value = false
    }
}

const goBack = () => {
    router.push('/notificationManagement')
}

onMounted(async () => {
    await loadTypes()
    await loadTemplate()
})
</script>

<style lang="scss" scoped>
.title {
    margin: 0 0 16px;
    color: var(--text-color--primary);
}

.scrollable-form {
    min-height: 0;
}

.form-scroll-area {
    width: 100%;
    padding: 24px;
    overflow: auto;
}

.image-substitution-section {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.image-header-row {
    display: flex;
    align-items: center;
    gap: 10px;
}

.selected-files-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    min-height: 36px;
}

.file-count {
    color: var(--text-color--secondary);
    font-size: 14px;
}

.action-button {
    background-color: var(--primary-color);
    color: var(--text-color--white);
    border: none;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    margin-top: 24px;
}
</style>
