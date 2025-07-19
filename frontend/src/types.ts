export type Interval = {
    start: string
    end: string
}

export type Banner = {
    characters: string[]
    image_url: string
}

export type BannerGroup = {
    index: number

    banners: Banner[]
    interval: Interval

    is_limited: boolean
    is_fest: boolean
    is_prediction: boolean
}