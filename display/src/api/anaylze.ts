import { http } from "@/utils/http";

export type ApiResult<T> = {
  code: number;
  data: T;
  msg: string;
};

export const ApiType = {
  //微博热搜榜
  WeiBoHotSearch: 1,

  // 微博要闻榜
  WeiBoEntertainment: 2,

  //   微博要闻榜
  WeiBoNews: 3,

  // 百度热搜
  Baidu: 4,

  // 知乎热搜
  Zhihu: 5,

  // 澎湃热搜
  PengPai: 6,

  // 今日头条
  TouTiao: 7,

  // 搜狗热搜
  Sougou: 8,

  // 抖音热搜
  Douyin: 9,

  // 哔哩哔哩热搜
  Bilibili: 10,

  // 快手热搜
  KuaiShou: 11,

  // 腾讯新闻热搜
  TencentNews: 12
};

export type HotSearchOriginDataItem = {
  title: string;
  ranl: number;
  time: number;
  hot_num: number;
};

export type HotSearchOriginData = {
  platform: number;
  time: number;
  data: HotSearchOriginDataItem[];
};

/**
 * 获取热搜的源数据
 * @param apiType 平台类型
 * @param start 开始时间戳
 * @param end 结束时间戳
 * @returns Promise<HotSearchOriginData>
 */
export const getHotSearchOriginData = (
  apiType: number,
  start: number,
  end: number
): Promise<ApiResult<HotSearchOriginData>> => {
  const params = { start, end };

  if (apiType == ApiType.WeiBoHotSearch) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/weibo", {
      params
    });
  }
  if (apiType == ApiType.WeiBoNews) {
    return http.request<ApiResult<HotSearchOriginData>>(
      "get",
      "/hot/weibo-news",
      {
        params
      }
    );
  }
  if (apiType == ApiType.WeiBoEntertainment) {
    return http.request<ApiResult<HotSearchOriginData>>(
      "get",
      "/hot/weibo-entertainment",
      { params }
    );
  }

  if (apiType == ApiType.Baidu) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/baidu", {
      params
    });
  }
  if (apiType == ApiType.Zhihu) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/zhihu", {
      params
    });
  }
  if (apiType == ApiType.PengPai) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/pengpai", {
      params
    });
  }
  if (apiType == ApiType.TouTiao) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/toutiao", {
      params
    });
  }
  if (apiType == ApiType.Sougou) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/sougou", {
      params
    });
  }
  if (apiType == ApiType.Douyin) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/douyin", {
      params
    });
  }
  if (apiType == ApiType.Bilibili) {
    return http.request<ApiResult<HotSearchOriginData>>(
      "get",
      "/hot/bilibili",
      { params }
    );
  }
  if (apiType == ApiType.KuaiShou) {
    return http.request<ApiResult<HotSearchOriginData>>(
      "get",
      "/hot/kuaishou",
      { params }
    );
  }
  if (apiType == ApiType.TencentNews) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/tencent", {
      params
    });
  }
  throw Error("apiType doesn't match!");
};

export type WordCloudHotNumItem = {
  timestamp: number;
  words: {
    word: string;
    hot_num: number;
  }[];
};

/**
 * 获取词云数据，根据热度排序
 *
 */
export const getWordCloudHotNum = (
  apiType: number,
  start: number,
  end: number
): Promise<ApiResult<WordCloudHotNumItem[]>> => {
  const params = {
    start,
    end
  };
  return http.request<ApiResult<WordCloudHotNumItem[]>>(
    "get",
    `/hot/word-cloud-hot-num/${apiType}`,
    { params }
  );
};

export type WordCloudNumItem = {
  timestamp: number;
  words: {
    word: string;
    num: number;
  }[];
};

/**
 * 获取词云数据，根据出现次数排序
 *
 */
export const getWordCloudNum = (
  apiType: number,
  start: number,
  end: number
): Promise<ApiResult<WordCloudNumItem[]>> => {
  const params = {
    start,
    end
  };
  return http.request<ApiResult<WordCloudNumItem[]>>(
    "get",
    `/hot/word-cloud-num/${apiType}`,
    { params }
  );
};

export type TrendingDataItem = {
  title: string;
  start_timestamp: number;
  end_timestamp: number;
  max_hot_num: number;
  avg_hot_num: number;
  min_hot_num: number;
  max_rank: number;
  min_rank: number;
  trending_list: {
    timestamp: number;
    hot_num: number;
    rank: number;
  }[];
};

/**
 * 获取变化趋势数据
 *
 */
export const getTrendingData = (
  apiType: number,
  title: string,
  start: number,
  end: number
): Promise<ApiResult<TrendingDataItem[]>> => {
  const params = {
    start,
    end,
    title_keyword: title
  };
  return http.request<ApiResult<TrendingDataItem[]>>(
    "get",
    `/hot/trending-data/${apiType}`,
    { params }
  );
};

export type WeiBoCategoryData = {
  category: string;
  values: {}[];
};

export const getWeiBoCategoryData = (
  apiType: number,
  start: number,
  end: number
): Promise<ApiResult<WeiBoCategoryData[]>> => {
  const params = {
    start,
    end
  };
  return http.request<ApiResult<TrendingDataItem[]>>(
    "get",
    `/hot/weibo-category-data/${apiType}`,
    { params }
  );
};
