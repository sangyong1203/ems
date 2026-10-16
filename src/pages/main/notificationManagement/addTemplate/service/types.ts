// SearchParams 템플릿 검색 파라미터
export type SearchParams = {
    pageNumber: number // 페이지 번호
    pageSize: number // 페이지 크기
    activeFlag?: string[] // 사용 여부 플래그
    searchType?: string // 검색 대상 필드
    searchKeyword?: string // 검색 키워드
    sortColumn?: string // 정렬 컬럼
    sortDirection?: string // 정렬 방향
}

// TemplateItem 알림 템플릿 상세 정보
export type TemplateItem = {
    id: number // 템플릿 ID
    type: string // 템플릿 유형
    typeId?: number // 템플릿 유형 ID
    title: string // 템플릿 제목
    body?: string // 본문 HTML/텍스트
    activeFlag: string[] // 사용 여부 플래그
    updatedAt: string // 수정 일시
}

// TemplateType 템플릿 분류 유형
export type TemplateType = {
    id: number // 유형 ID
    type: string // 유형 코드
    description: string // 유형 설명
}
