"use client";

import React, { useState, useEffect, useCallback } from "react";
import { format } from "d3-format";
import { timeFormat } from "d3-time-format";
import { scaleTime } from "d3-scale";
import {
  ChartCanvas,
  Chart,
  CandlestickSeries,
  XAxis,
  YAxis,
  CrossHairCursor,
  MouseCoordinateX,
  MouseCoordinateY,
  OHLCTooltip,
  LineSeries,
  BarSeries,
} from "react-financial-charts";
import {
  fetchKlineData,
  KLineDataItem,
  fetchMACDData,
  fetchRSIData,
  MACDData,
  RSIData,
} from "./api/klineData";

interface ChartData extends KLineDataItem {
  date: Date;
  macd?: number;
  signal?: number;
  histogram?: number;
  rsi?: number;
}

export default function ImprovedChart() {
  const [interval, setInterval] = useState<string>("1m");
  const [chartData, setChartData] = useState<ChartData[]>([]);
  const [error, setError] = useState<string>("");
  const [macdData, setMACDData] = useState<MACDData>({
    macd: [],
    signal: [],
    histogram: [],
    timestamps: [],
  });
  const [rsiData, setRSIData] = useState<RSIData>({ rsi: [], timestamps: [] });
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isSelectOpen, setIsSelectOpen] = useState<boolean>(false);

  const getTimeRange = () => {
    const end = new Date();
    const start = new Date(end.getTime() - 60 * 60 * 1000); // 1 hour ago
    return { start: start.getTime(), end: end.getTime() };
  };

  const fetchData = useCallback(async () => {
    setIsLoading(true);
    try {
      const { start, end } = getTimeRange();
      const data = await fetchKlineData(interval, start, end);
      const macd = await fetchMACDData("BTCUSDT", interval, start, end);
      const rsi = await fetchRSIData("BTCUSDT", interval, start, end);

      if (data && data.length > 0) {
        setMACDData(
          macd || { macd: [], signal: [], histogram: [], timestamps: [] }
        );
        setRSIData(rsi || { rsi: [], timestamps: [] });
        setChartData(formatData(data, macd, rsi));
        setError("");
      } else {
        setChartData([]);
        setError("No data available for the selected time range");
      }
    } catch (err) {
      setChartData([]);
      setError("Failed to fetch data");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, [interval]);

  useEffect(() => {
    fetchData();
    const intervalId = window.setInterval(fetchData, 60000); // Fetch data every minute

    return () => window.clearInterval(intervalId);
  }, [fetchData]);

  const formatData = (
    data: KLineDataItem[],
    macd: MACDData | null,
    rsi: RSIData | null
  ): ChartData[] => {
    return data.map((item, index) => ({
      ...item,
      date: new Date(item.openTime),
      macd: macd?.macd?.[index] ?? undefined,
      signal: macd?.signal?.[index] ?? undefined,
      histogram: macd?.histogram?.[index] ?? undefined,
      rsi: rsi?.rsi?.[index] ?? undefined,
    }));
  };

  const xAccessor = (d: ChartData) => d.date;

  const xExtents = React.useMemo(() => {
    if (chartData.length > 0) {
      return [
        xAccessor(chartData[0]),
        xAccessor(chartData[chartData.length - 1]),
      ];
    }
    return [new Date(0), new Date()]; // Default range if no data
  }, [chartData]);

  const xScale = scaleTime();

  return (
    <div className="container mx-auto p-4">
      <div className="bg-white shadow-md rounded-lg p-6 mb-6">
        <h2 className="text-2xl font-bold mb-4">BTC/USDT Candlestick Chart</h2>
        <div className="flex items-center justify-between mb-4">
          <div className="relative">
            <button
              className="bg-white border border-gray-300 rounded-md px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              onClick={() => setIsSelectOpen(!isSelectOpen)}
            >
              {interval}
            </button>
            {isSelectOpen && (
              <div className="absolute mt-1 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5">
                <div
                  className="py-1"
                  role="menu"
                  aria-orientation="vertical"
                  aria-labelledby="options-menu"
                >
                  {["1m", "5m", "15m", "1h"].map((option) => (
                    <button
                      key={option}
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 w-full text-left"
                      role="menuitem"
                      onClick={() => {
                        setInterval(option);
                        setIsSelectOpen(false);
                      }}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
          <button
            className={`bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded ${
              isLoading ? "opacity-50 cursor-not-allowed" : ""
            }`}
            onClick={fetchData}
            disabled={isLoading}
          >
            {isLoading ? "Loading..." : "Refresh"}
          </button>
        </div>

        {error && (
          <div
            className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4"
            role="alert"
          >
            <strong className="font-bold">Error: </strong>
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        {chartData.length > 0 && (
          <div className="space-y-6 overflow-x-auto">
            <ChartCanvas
              height={400}
              ratio={1}
              width={800}
              margin={{ left: 50, right: 50, top: 10, bottom: 30 }}
              data={chartData}
              displayXAccessor={xAccessor}
              xAccessor={xAccessor}
              xExtents={xExtents}
              seriesName={"BTC/USDT"}
              xScale={xScale}
            >
              <Chart id={1} yExtents={(d) => [d.high, d.low]}>
                <XAxis axisAt="bottom" orient="bottom" ticks={6} />
                <YAxis axisAt="left" orient="left" ticks={5} />
                <CandlestickSeries />
                <MouseCoordinateX
                  at="bottom"
                  orient="bottom"
                  displayFormat={timeFormat("%Y-%m-%d %H:%M")}
                />
                <MouseCoordinateY
                  at="left"
                  orient="left"
                  displayFormat={format(".2f")}
                />
                <OHLCTooltip origin={[-40, 0]} />
              </Chart>
              <CrossHairCursor />
            </ChartCanvas>

            <ChartCanvas
              height={150}
              ratio={1}
              width={800}
              margin={{ left: 50, right: 50, top: 10, bottom: 30 }}
              data={chartData}
              displayXAccessor={xAccessor}
              xAccessor={xAccessor}
              xExtents={xExtents}
              seriesName={"MACD"}
              xScale={xScale}
            >
              <Chart id={2} yExtents={(d) => [d.macd, d.signal, d.histogram]}>
                <XAxis axisAt="bottom" orient="bottom" />
                <YAxis axisAt="left" orient="left" ticks={5} />
                <LineSeries yAccessor={(d) => d.macd} strokeStyle="#ff7f0e" />
                <LineSeries yAccessor={(d) => d.signal} strokeStyle="#2ca02c" />
                <BarSeries
                  yAccessor={(d) => d.histogram}
                  fillStyle={(d) => (d.histogram >= 0 ? "#2ca02c" : "#ff7f0e")}
                />
                <MouseCoordinateY
                  at="left"
                  orient="left"
                  displayFormat={format(".2f")}
                />
              </Chart>
            </ChartCanvas>

            <ChartCanvas
              height={150}
              ratio={1}
              width={800}
              margin={{ left: 50, right: 50, top: 10, bottom: 30 }}
              data={chartData}
              displayXAccessor={xAccessor}
              xAccessor={xAccessor}
              xExtents={xExtents}
              seriesName={"RSI"}
              xScale={xScale}
            >
              <Chart id={3} yExtents={[0, 100]}>
                <XAxis axisAt="bottom" orient="bottom" />
                <YAxis axisAt="left" orient="left" ticks={5} />
                <LineSeries yAccessor={(d) => d.rsi} strokeStyle="#8884d8" />
                <MouseCoordinateY
                  at="left"
                  orient="left"
                  displayFormat={format(".2f")}
                />
              </Chart>
            </ChartCanvas>
          </div>
        )}
      </div>
    </div>
  );
}
