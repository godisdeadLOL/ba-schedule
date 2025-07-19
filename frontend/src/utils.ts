import type { Interval } from "./types"

function getCurrentTime() {
    const now = new Date()
    return now
}

export function dateToIsoTime(date: Date) {
    const converted = date.toISOString()
    return converted.substring(0, converted.length-1)
}

export function formatTimestamp(timestamp: string, local: boolean = false) {
    const locale = "ru-RU"
    const options: any = {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
    }

    return new Date(timestamp + (local ? 'Z' : '')).toLocaleString(locale, options)
}

export function formatTimestampMonth(timestamp: string, local: boolean = false) {
    const locale = "en-EN"
    const options: any = { year: "numeric", month: "short" }

    return new Date(timestamp + (local ? 'Z' : '')).toLocaleDateString(locale, options)
}

export function isCurrentInterval(interval: Interval) {
    const now = getCurrentTime()
    return now > new Date(interval.start + "Z") && now < new Date(interval.end + "Z")
}

export function isUpcomingInterval(interval: Interval) {
    const now = getCurrentTime()
    return now < new Date(interval.end + "Z")
}

export function isPreviousInterval(interval: Interval) {
    const now = getCurrentTime()
    return now > new Date(interval.start + "Z")
}

export function getIntervalStatus(interval: Interval) {
    const isCurrent = isCurrentInterval(interval)
    const isPrevious = isPreviousInterval(interval)
    return isCurrent ? "Current" : isPrevious ? "Previous" : "Prediction"
}

function pluralize(amount: number, one: string, many: string) {
    return amount > 1 ? many : one
}

function getTimeUntilTimestamp(timestamp: string) {
    let seconds = (new Date(timestamp + 'Z').getTime() - getCurrentTime().getTime()) / 1000.0

    if (seconds < 0) return null

    const hours = Math.round(seconds / 60 / 60)
    const days = Math.round(hours / 24)
    const months = Math.round(days / 30) // примерно сойдет
    const years = Math.round(months / 12)

    if (hours < 1) return "soon"
    else if (hours < 24) return `in ${hours} ${pluralize(hours, 'hour', 'hours')}`
    else if (days < 30) return `in ${days} ${pluralize(days, 'day', 'days')}`
    else if (months < 12) return `in ${months} ${pluralize(months, 'month', 'months')}`
    else return `in ${years} ${pluralize(months, 'year', 'years')}`
}

export function getCountdownMessage(interval: Interval) {
    if (isCurrentInterval(interval)) {
        return `Ends ${getTimeUntilTimestamp(interval.end)}`
    }
    else {
        const value = getTimeUntilTimestamp(interval.start)
        if (!value) return undefined

        return `Starts ${value}`
    }
}