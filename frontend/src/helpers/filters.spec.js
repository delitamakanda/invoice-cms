import { describe, expect, it } from 'vitest'
import filters from './filters'

describe('filters', () => {
  it('formats a currency value with two decimals and the euro sign', () => {
    expect(filters.currency(12.5)).toBe('12.50€')
  })

  it('returns a dash for a non-numeric currency value', () => {
    expect(filters.currency('abc')).toBe('-')
  })

  it('formats a decimal value with two decimals', () => {
    expect(filters.decimal(3)).toBe('3.00')
  })
})
