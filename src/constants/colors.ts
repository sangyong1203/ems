export type Union<T> = T[keyof T]

export const COLOR_TYPE = {
    PRIMARY: '#e76dff',
    SECONDARY: '#15e0b7',
  RED:'#f96060',
    ORANGE: '#f19c4d',
    BLUE: '#4ca5d7',
    GREEN: '#56ba64',
    TEAL: '#009a93',
    YELLOW: '#fbbc05',
    PURPLE: '#68127a',
    NAVY: '#0e306d',
    GRAY: '#c9cbcf',
    MINT: '#85e0d2',
    RED80:'#f96060d9',
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
  RED:'#f96060',
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





