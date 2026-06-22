import { type RouteRecordRaw } from 'vue-router'

export const routes: RouteRecordRaw[] = [

    {
        path: '/login',
        name: 'login',
        component: () => import('@/pages/login/LoginPage.vue'),
    },
    {
        path: '/password-reset/:verificationToken',
        name: 'passwordReset',
        component: () => import('@/pages/login/PasswordReset.vue'),
    },
    {
        path: '/',
        redirect: { name: 'login' },
        name: 'main',
        component: () => import('@/pages/main/MainPage.vue'),
        children: [
            {
                path: '/dashboard',
                name: 'dashboard',
                component: () => import('@/pages/main/dashboard/DashboardPage.vue'),
            },
            {
                path: '/solar',
                name: 'solar',
                component: () => import('@/pages/main/solar/SolarPage.vue'),
            },
            {
                path: '/ess',
                name: 'ess',
                component: () => import('@/pages/main/ess/EssPage.vue'),
            },
            {
                path: '/power-flow',
                name: 'powerFlow',
                component: () => import('@/pages/main/powerFlow/PowerFlowPage.vue'),
            },
            {
                path: '/trend',
                name: 'trend',
                component: () => import('@/pages/main/trend/TrendPage.vue'),
            },
            {
                path: '/device-management',
                name: 'deviceManagement',
                component: () => import('@/pages/main/deviceManagement/DeviceManagementPage.vue'),
            },
            {
                path: '/maintenance-management',
                name: 'maintenanceManagement',
                component: () => import('@/pages/main/maintenanceManagement/MaintenanceManagementPage.vue'),
            },
            {
                path: '/alarm-history',
                name: 'alarmHistory',
                component: () => import('@/pages/main/alarmHistory/AlarmHistoryPage.vue'),
            },
            {
                path: '/operation-report',
                name: 'operationReport',
                component: () => import('@/pages/main/operationReport/OperationReportPage.vue'),
            },
            {
                path: '/settings',
                name: 'settings',
                component: () => import('@/pages/main/settings/SettingsPage.vue'),
            },
        ],
    },


    {
        path: '/:pathMatch(.*)*',
        redirect: '/404',
    },

    // 
    { path: '/403', name: '403', component: () => import('@/pages/errorPage/ForbiddenPage.vue') },
    { path: '/404', name: '404', component: () => import('@/pages/errorPage/NotFoundPage.vue') },
    { path: '/500', name: '500', component: () => import('@/pages/errorPage/ServerErrorPage.vue') },
]
