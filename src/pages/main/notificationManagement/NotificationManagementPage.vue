<template>
    <PageBody>
        <SearchBox :on-search="searchData">
            <LabelFormItem label="In Use">
                <el-checkbox-group v-model="searchParams.activeFlag" @change="checkInUse">
                    <el-checkbox label="Yes" value="Y" />
                    <el-checkbox label="No" value="N" />
                </el-checkbox-group>
            </LabelFormItem>
        </SearchBox>
        <ContentBlock>
            <OperationBox :title="'Total Items'" :total="addComma(totalCount)" bottom-line>
                <el-button type="primary" @click="addTemplate">Add Template</el-button>
            </OperationBox>
            <el-table
                v-loading="isTableLoading"
                :data="tableData"
                border
                stripe
                style="width: 100%"
                :empty-text="isTableLoading ? '' : 'No Data'"
                element-loading-text="Loading..."
                :element-loading-svg="loadingSvgContent"
                :element-loading-svg-view-box="loadingSvgViewBox"
                element-loading-background="rgba(255, 255, 255, 0.82)"
                @row-click="editTemplate"
            >
                <el-table-column prop="type" label="Type" />
                <el-table-column prop="title" label="Title" />
                <el-table-column prop="activeFlag" label="In Use" />
                <el-table-column prop="updatedAt" label="Last Updated">
                    <template #default="{ row }">
                        {{ row.updatedAt ? localeDateFormat(row.updatedAt, 'YYYY-MM-DD HH:mm:ss') : '' }}
                    </template>
                </el-table-column>
            </el-table>
        </ContentBlock>
    </PageBody>
</template>
<script lang="ts" setup>
import router from '@/router'
import { onMounted, reactive, ref } from 'vue'
import type { CheckboxValueType } from 'element-plus'
import notificationManagementApi from './service/notificationManagement.api'
import type { SearchParams, TemplateList } from './service/notificationManagement.types'
import { Message, Notification } from '@/composables/useFeedback'
import { loadingSvgContent, loadingSvgViewBox } from '@/composables/useProgressBar'
import { addComma, localeDateFormat } from '@/utils'

const isTableLoading = ref(true) // 테이블 로딩 상태
const tableData = ref<TemplateList[]>([]) // 알림 템플릿 목록 데이터
const totalCount = ref(0) // 전체 알림 템플릿 건수

// addTemplate 신규 템플릿 등록 페이지로 이동
const addTemplate = () => {
    router.push({
        path: '/notificationManagement/templateList/addTemplate',
        state: { type: 'create' },
    })
}

// editTemplate 템플릿 상세/수정 페이지로 이동
const editTemplate = (row: any) => {
    router.push({
        path: '/notificationManagement/templateList/addTemplate',
        state: { type: 'edit', templateId: row.id },
    })
}

const searchParams = reactive<SearchParams>({ // 알림 템플릿 검색 조건
    activeFlag: ['Y', 'N'],
    searchType: '',
    pageNumber: 1,
    pageSize: 10,
    sortColumn: '',
    sortDirection: '',
})

// onMounted 초기 템플릿 목록 조회
onMounted(async () => {
    await getList()
})

// searchData 검색 조건 검증 후 목록 재조회
const searchData = () => {
    if (!searchParams.activeFlag?.length) {
        Notification.warning('Please select at least one option.')
        return
    }

    searchParams.pageNumber = 1
    getList()
}

const previousActiveFlag = ref<string[]>([...(searchParams.activeFlag || [])]) // 직전 사용 여부 선택값 캐시

// checkInUse 사용 여부 체크박스 변경 시 유효성 검증 및 조회
const checkInUse = (values: CheckboxValueType[]) => {
    const selected = values.map(value => String(value))

    if (selected.length === 0) {
        searchParams.activeFlag = [...previousActiveFlag.value]
        showCheckWarning()
        return
    }

    previousActiveFlag.value = [...selected]

    getList()
}

// showCheckWarning 최소 선택 알림 표시
const showCheckWarning = () => {
    Notification.warning('Please select at least one.')
    return
}

// getList 알림 템플릿 목록 API 조회
const getList = async () => {
    if (searchParams.searchType == undefined) {
        searchParams.searchType = ''
    }

    isTableLoading.value = true
    try {
        const res = await notificationManagementApi.getList(searchParams)

        if (res.result !== 'success') {
            tableData.value = []
            totalCount.value = 0
            Message.warning(res.resultMessage || 'Failed to load templates.')
            return
        }

        tableData.value = res.data.list
        totalCount.value = res.data.totalCount
    } catch {
        tableData.value = []
        totalCount.value = 0
        Message.error('Failed to load templates.')
    } finally {
        isTableLoading.value = false
    }
}
</script>

<style lang="scss" scoped>
:deep(.search-box .text-right) {
    display: none;
}
</style>
