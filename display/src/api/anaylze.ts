import { ApiResult, ApiType, HotSearchOriginData } from './anaylze';
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
  const data = { start, end };

  if (apiType == ApiType.WeiBoHotSearch) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/weibo", { data });
  }
  if (apiType == ApiType.WeiBoNews) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/weibo-news", {
      data
    });
  }
  if (apiType == ApiType.WeiBoEntertainment) {
    return http.request<ApiResult<HotSearchOriginData>>(
      "get",
      "/hot/weibo-entertainment",
      { data }
    );
  }

  if (apiType == ApiType.Baidu) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/baidu", { data });
  }
  if (apiType == ApiType.Zhihu) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/zhihu", { data });
  }
  if (apiType == ApiType.PengPai) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/pengpai", { data });
  }
  if (apiType == ApiType.TouTiao) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/toutiao", { data });
  }
  if (apiType == ApiType.Sougou) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/sougou", { data });
  }
  if (apiType == ApiType.Douyin) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/douyin", { data });
  }
  if (apiType == ApiType.Bilibili) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/bilibili", { data });
  }
  if (apiType == ApiType.KuaiShou) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/kuaishou", { data });
  }
  if (apiType == ApiType.TencentNews) {
    return http.request<ApiResult<HotSearchOriginData>>("get", "/hot/tencent", { data });
  }
  throw Error("apiType doesn't match!");
};



export type WordCloudResultItem = {
  timestamp: number,
  words: {
    word: string,
    hot_num: number,
  }[]
};


export const getWordCloud = (
  apiType: number,
  start: number,
  end: number
): Promise<ApiResult<WordCloudResultItem[]>> => {
  const data = {
    start, end
  };
  return http.request<ApiResult<WordCloudResultItem[]>>("get", `/hot/word-cloud-hot-num/${apiType}`, { data });
};