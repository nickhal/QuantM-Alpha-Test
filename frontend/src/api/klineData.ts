const API_BASE_URL = "http://localhost:5001/api";

export interface KLineDataItem {
  openTime: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  closeTime: number;
}

export interface MACDData {
  macd: number[];
  signal: number[];
  histogram: number[];
  timestamps: number[];
}

export interface RSIData {
  rsi: number[];
  timestamps: number[];
}

export const fetchKlineData = async (
  interval: string,
  startTime: number,
  endTime: number
): Promise<KLineDataItem[]> => {
  const symbol = "BTCUSDT";
  const response = await fetch(
    `${API_BASE_URL}/kline?symbol=${symbol}&interval=${interval}&startTime=${startTime}&endTime=${endTime}`
  );
  if (!response.ok) {
    throw new Error("Failed to fetch kline data");
  }
  return response.json();
};

export const fetchMACDData = async (
  symbol: string,
  interval: string,
  startTime: number,
  endTime: number
): Promise<MACDData> => {
  const response = await fetch(
    `${API_BASE_URL}/macd?symbol=${symbol}&interval=${interval}&startTime=${startTime}&endTime=${endTime}`
  );
  if (!response.ok) {
    throw new Error("Failed to fetch MACD data");
  }
  return response.json();
};

export const fetchRSIData = async (
  symbol: string,
  interval: string,
  startTime: number,
  endTime: number
): Promise<RSIData> => {
  const response = await fetch(
    `${API_BASE_URL}/rsi?symbol=${symbol}&interval=${interval}&startTime=${startTime}&endTime=${endTime}`
  );
  if (!response.ok) {
    throw new Error("Failed to fetch RSI data");
  }
  return response.json();
};

export const fetchSymbols = async (): Promise<string[]> => {
  const response = await fetch(`${API_BASE_URL}/symbols`);
  if (!response.ok) {
    throw new Error("Failed to fetch symbols");
  }
  return response.json();
};
