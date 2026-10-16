import { fetchApi } from '@/http'
import type { PayloadModel } from '@/http/type'
import type { DailyReportResponse, ReportStatisticsResponse, ReportSummaryResponse } from './operationReport.types'

export default {
    // getDailyReport 특정 일자의 일간 운영 보고서 조회
    async getDailyReport(date = ''): Promise<DailyReportResponse> {
        const payload: PayloadModel = { query: { date } }
        return await fetchApi().get('/api/reports/daily', { payload })
    },

    // getSummary 지정 기간의 운영 보고서 종합 요약 조회
    async getSummary(dateFrom = '', dateTo = ''): Promise<ReportSummaryResponse> {
        const payload: PayloadModel = { query: { dateFrom, dateTo } }
        return await fetchApi().get('/api/reports/summary', { payload })
    },

    // getStatistics 지정 기간의 운영 보고서 통계 및 차트 시계열 데이터 조회
    async getStatistics(dateFrom = '', dateTo = ''): Promise<ReportStatisticsResponse> {
        const payload: PayloadModel = { query: { dateFrom, dateTo } }
        return await fetchApi().get('/api/reports/statistics', { payload })
    },
}
