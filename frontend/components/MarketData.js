export default function MarketData({ data }) {
    return (
      <div className="bg-white p-4 rounded shadow">
        <h2 className="text-xl font-bold mb-4">Current Market Data</h2>
        <div>
          {data.BTCUSDT ? (
            <div className="mb-2">
              <span className="font-semibold">BTC/USDT: </span>
              <span>{data.BTCUSDT.price || data.BTCUSDT.lastPrice}</span>
            </div>
          ) : (
            <p>Loading BTC data...</p>
          )}
          {data.ETHUSDT ? (
            <div className="mb-2">
              <span className="font-semibold">ETH/USDT: </span>
              <span>{data.ETHUSDT.price || data.ETHUSDT.lastPrice}</span>
            </div>
          ) : (
            <p>Loading ETH data...</p>
          )}
        </div>
      </div>
    );
  }
  