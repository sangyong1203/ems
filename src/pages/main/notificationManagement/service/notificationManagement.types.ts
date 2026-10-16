import type { APIResponse } from '@/http/type'

// TemplateList 알림 템플릿 목록 행 항목
export type TemplateList = {
    id: number // 템플릿 ID
    type: string // 템플릿 유형
    title: string // 템플릿 제목
    activeFlag: string[] // 사용 여부 플래그 배열 (Y, N)
    updatedAt: string // 최종 수정 일시
}

// TemplateItem 알림 템플릿 상세 정보
export type TemplateItem = {
    id: number // 템플릿 ID
    type: string // 템플릿 유형명
    typeId?: number // 템플릿 유형 ID
    title: string // 템플릿 제목
    body?: string // 템플릿 본문 내용
    activeFlag: string[] // 사용 여부 플래그
    updatedAt: string // 최종 수정 일시
}

// TemplateType 알림 템플릿 분류 유형
export type TemplateType = {
    id: number // 유형 ID
    type: string // 유형 코드
    description: string // 유형 설명
}

// SearchParams 알림 템플릿 검색 파라미터
export type SearchParams = {
    pageNumber: number // 페이지 번호
    pageSize: number // 페이지 크기
    activeFlag?: string[] // 사용 여부 필터
    searchType?: string // 검색 대상 유형
    searchKeyword?: string // 검색 키워드
    sortColumn?: string // 정렬 기준 컬럼
    sortDirection?: string // 정렬 방향 (ASC/DESC)
}

// TemplateListResponse 알림 템플릿 목록 응답
export type TemplateListResponse = Omit<APIResponse, 'data'> & {
    data: {
        list: TemplateList[] // 템플릿 목록
        totalCount: number // 총 건수
    }
}

// TemplateDetailResponse 알림 템플릿 상세 응답
export type TemplateDetailResponse = Omit<APIResponse, 'data'> & {
    data: TemplateItem | null // 템플릿 상세
}

// TemplateTypesResponse 알림 템플릿 유형 목록 응답
export type TemplateTypesResponse = Omit<APIResponse, 'data'> & {
    data: TemplateType[] // 템플릿 유형 목록
}
