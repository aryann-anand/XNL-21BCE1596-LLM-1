import { useEffect, useState } from 'react';
import Header from '../components/Header';
import MarketData from '../components/MarketData';
import TradeDropdown from '../components/TradeDropdown';
import ChatBox from '../components/ChatBox';
import TransactionLog from '../components/TransactionLog';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS, Title, Tooltip, Legend, LineElement,
  CategoryScale, LinearScale, PointElement
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);

export default function Dashboard() {
  const [marketData, setMarketData] = useState({});
  const [selectedSymbol, setSelectedSymbol] = useState('BTCUSDT');
  const [tradeAmount, setTradeAmount] = useState(0.1);
  const [transactionLogs, setTransactionLogs] = useState([]);
  const [historicalData, setHistoricalData] = useState([]);

  const fetchMarketData = async () => {
    const res = await fetch("http://localhost:8000/api/market-data");
    const data = await res.json();
    setMarketData(data);
  };

  const fetchTransactionLogs = async () => {
    const res = await fetch("http://localhost:8000/api/transaction-logs");
    const data = await res.json();
    if (data.logs) {
      const logsArray = data.logs.split("\n")
        .filter(line => line.trim() !== "")
        .map(line => JSON.parse(line));
      setTransactionLogs(logsArray);
    }
  };

  const fetchHistoricalData = async () => {
    const res = await fetch(`http://localhost:8000/api/backtesting?symbol=${selectedSymbol}`);
    const data = await res.json();
    if (data.historical_data) {
      setHistoricalData(data.historical_data);
    }
  };

  useEffect(() => {
    fetchMarketData();
    fetchHistoricalData();
    fetchTransactionLogs();
    const interval = setInterval(() => {
      fetchMarketData();
      fetchTransactionLogs();
    }, 10000);
    return () => clearInterval(interval);
  }, []);

  // Update historical data when selected crypto changes
  useEffect(() => {
    fetchHistoricalData();
  }, [selectedSymbol]);

  const handleTrade = async () => {
    const res = await fetch("http://localhost:8000/api/simulate-trade", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ symbol: selectedSymbol, amount: tradeAmount })
    });
    const data = await res.json();
    alert(`Trade executed:\n${JSON.stringify(data.trade, null, 2)}`);
    fetchTransactionLogs();
  };

  const chartData = {
    labels: historicalData.map((d, i) => `T${i + 1}`),
    datasets: [
      {
        label: `${selectedSymbol} Price Trend`,
        data: historicalData.map(d => d.price),
        borderColor: 'rgba(75,192,192,1)',
        fill: false
      }
    ]
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      <div className="p-4 grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="col-span-2 space-y-4">
          <MarketData data={marketData} />
          <div className="bg-white p-4 rounded shadow">
            <h2 className="text-xl font-bold mb-4">Historical Trend for {selectedSymbol}</h2>
            {historicalData.length > 0 ? <Line data={chartData} /> : <p>Loading historical trend...</p>}
          </div>
          <div className="bg-white p-4 rounded shadow">
            <h2 className="text-xl font-bold mb-4">Simulate Trade</h2>
            <TradeDropdown selectedSymbol={selectedSymbol} setSelectedSymbol={setSelectedSymbol} />
            <div className="mt-2">
              <label className="font-semibold">Amount:</label>
              <input 
                type="number" 
                value={tradeAmount} 
                onChange={(e) => setTradeAmount(parseFloat(e.target.value))}
                className="border border-gray-300 p-2 rounded ml-2"
              />
            </div>
            <button onClick={handleTrade} className="mt-4 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
              Execute Trade
            </button>
          </div>
          <TransactionLog logs={transactionLogs} />
        </div>
        <div className="col-span-1">
          <ChatBox />
        </div>
      </div>
    </div>
  );
}
