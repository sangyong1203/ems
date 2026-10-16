export type Union<T> = T[keyof T]

// ============================================================================
// Tier 1: Primitive Palette
// ============================================================================
export const PRIMITIVE_COLORS = {
  violet: {
    500: '#e76dff',
    600: '#cb4ee3',
    700: '#68127a',
    800: '#3e2576',
    900: '#2d1f3d',
    950: '#12021f',
  },
  teal: {
    400: '#15e0b7',
    500: '#12c9a4',
    600: '#009a93',
    700: '#12353b',
  },
  cyan: {
    400: '#35d8ff',
  },
  mint: {
    300: '#85e0d2',
  },
  slate: {
    950: '#151822',
    900: '#171a24',
    850: '#181b25',
    800: '#1d2130',
    750: '#272727',
    700: '#18202b',
  },
  status: {
    red: '#ff383c',
    redLight: '#ff7478',
    orange: '#f19c4d',
    yellow: '#fbbc05',
    green: '#56ba64',
    blue: '#4ca5d7',
    navy: '#0e306d',
  },
  gray: {
    white: '#ffffff',
    50: '#f5f5f5',
    100: '#f4f1f8',
    200: '#d8d1e0',
    300: '#c9c1d4',
    400: '#9f98aa',
    500: '#9c9c9c',
    black: '#000000',
  },
} as const

// ============================================================================
// Tier 2: Semantic Tokens (Meaning & Role Based)
// ============================================================================
export const SEMANTIC_COLORS = {
  brand: {
    primary: PRIMITIVE_COLORS.violet[500],
    secondary: PRIMITIVE_COLORS.teal[400],
    accent: PRIMITIVE_COLORS.violet[500],
    cyan: PRIMITIVE_COLORS.teal[400],
  },
  surface: {
    deep: PRIMITIVE_COLORS.slate[950],
    base: PRIMITIVE_COLORS.slate[900],
    panel: PRIMITIVE_COLORS.slate[850],
    elevated: PRIMITIVE_COLORS.slate[800],
    glass: 'rgba(24, 27, 37, 0.48)',
  },
  text: {
    high: PRIMITIVE_COLORS.gray.white,
    primary: PRIMITIVE_COLORS.gray[50],
    strong: PRIMITIVE_COLORS.gray[100],
    body: PRIMITIVE_COLORS.gray[200],
    secondary: PRIMITIVE_COLORS.gray[300], // ECharts 라벨 및 축 텍스트
    muted: PRIMITIVE_COLORS.gray[400],
    placeholder: 'rgba(255, 255, 255, 0.38)',
  },
  border: {
    subtle: 'rgba(255, 255, 255, 0.08)',
    strong: 'rgba(255, 255, 255, 0.16)',
    brand: 'rgba(231, 109, 255, 0.24)',
    focus: '#dedede',
  },
  status: {
    danger: PRIMITIVE_COLORS.status.red,
    warning: PRIMITIVE_COLORS.status.orange,
    caution: PRIMITIVE_COLORS.status.yellow,
    success: PRIMITIVE_COLORS.status.green,
    info: PRIMITIVE_COLORS.status.blue,
  },
  // EMS Domain Specific
  domain: {
    solar: PRIMITIVE_COLORS.teal[400],      // 태양광 발전 (#15e0b7)
    battery: PRIMITIVE_COLORS.violet[500],  // ESS 배터리 (#e76dff)
    grid: PRIMITIVE_COLORS.status.blue,     // 계통 Grid (#4ca5d7)
    load: PRIMITIVE_COLORS.status.orange,   // 부하 소비 (#f19c4d)
  },
} as const

// ============================================================================
// ECharts 표준 테마 토큰
// ============================================================================
export const CHART_THEME = {
  textColor: SEMANTIC_COLORS.text.secondary, // '#c9c1d4'
  gridLineColor: SEMANTIC_COLORS.border.subtle, // 'rgba(255, 255, 255, 0.08)'
  axisLineColor: SEMANTIC_COLORS.border.strong, // 'rgba(255, 255, 255, 0.16)'
  tooltip: {
    backgroundColor: 'rgba(255, 255, 255, 0.92)',
    borderWidth: 0,
    textStyle: {
      color: '#18202b',
    },
  },
  severity: {
    CRITICAL: 'rgba(255, 107, 143, 0.72)',
    WARNING: 'rgba(231, 109, 255, 0.72)',
    INFO: 'rgba(21, 224, 183, 0.72)',
  },
  // 기본 표준 계열 팔레트
  palette: [
    SEMANTIC_COLORS.domain.solar, // #15e0b7 (Solar / Teal)
    SEMANTIC_COLORS.domain.battery, // #e76dff (Battery / Magenta)
    SEMANTIC_COLORS.domain.grid, // #4ca5d7 (Grid / Blue)
    SEMANTIC_COLORS.domain.load, // #f19c4d (Load / Orange)
    SEMANTIC_COLORS.status.success, // #56ba64 (Green)
  ],
} as const

// ============================================================================
// Legacy Aliases (기존 코드 100% 호환성 유지)
// ============================================================================
export const COLOR_TYPE = {
  PRIMARY: '#e76dff',
  SECONDARY: '#15e0b7',
  RED: '#f96060',
  ORANGE: '#f19c4d',
  BLUE: '#4ca5d7',
  GREEN: '#56ba64',
  TEAL: '#009a93',
  YELLOW: '#fbbc05',
  PURPLE: '#68127a',
  NAVY: '#0e306d',
  GRAY: '#c9cbcf',
  MINT: '#85e0d2',
  RED80: '#f96060d9',
  ORANGE80: '#f19c4dd9',
  BLUE80: '#4ca5d7d9',
  GREEN80: '#56ba64d9',
  TEAL80: '#009a93d9',
  YELLOW80: '#fbbc05d9',
  PURPLE80: '#68127ad9',
  NAVY80: '#0e306dd9',
  GRAY80: '#c9cbcfd9',
  MINT80: '#85e0d2d9',
} as const

export const CHART_COLOR = {
  PRIMARY: '#e76dff',
  SECONDARY: '#15e0b7',
  RED: '#f96060',
  ORANGE: '#f19c4d',
  BLUE: '#4ca5d7',
  GREEN: '#56ba64',
  TEAL: '#009a93',
  YELLOW: '#fbbc05',
  PURPLE: '#68127a',
  NAVY: '#0e306d',
  GRAY: '#c9cbcf',
} as const

export type ChartColor = Union<typeof CHART_COLOR>
