export default function TradeDropdown({ selectedSymbol, setSelectedSymbol }) {
    return (
      <div>
        <label className="font-semibold mr-2">Select Crypto:</label>
        <select 
          value={selectedSymbol} 
          onChange={(e) => setSelectedSymbol(e.target.value)}
          className="border border-gray-300 p-2 rounded"
        >
          <option value="BTCUSDT">BTC/USDT</option>
          <option value="ETHUSDT">ETH/USDT</option>
        </select>
      </div>
    );
  }
  