import { fetchApi } from '@/http'
import type { PayloadModel } from '@/http/type'
import type { DailyReportResponse, ReportStatisticsResponse, ReportSummaryResponse } from './operationReport.types'

export default {
    async getDailyReport(date = ''): Promise<DailyReportResponse> {
        const payload: PayloadModel = { query: { date } }
        return await fetchApi().get('/api/reports/daily', { payload })
    },

    async getSummary(dateFrom = '', dateTo = ''): Promise<ReportSummaryResponse> {
        const payload: PayloadModel = { query: { dateFrom, dateTo } }
        return await fetchApi().get('/api/reports/summary', { payload })
    },
    async getStatistics(dateFrom = '', dateTo = ''): Promise<ReportStatisticsResponse> {
        const payload: PayloadModel = { query: { dateFrom, dateTo } }
        return await fetchApi().get('/api/reports/statistics', { payload })
    },
}
