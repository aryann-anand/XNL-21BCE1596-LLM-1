export default function TransactionLog({ logs }) {
    return (
      <div className="bg-white p-4 rounded shadow">
        <h2 className="text-xl font-bold mb-4">Transaction Log</h2>
        <div className="max-h-64 overflow-y-auto">
          {logs.length === 0 ? (
            <p>No transactions yet.</p>
          ) : (
            logs.map((log, index) => (
              <div key={index} className="mb-2 border-b border-gray-200 pb-2">
                <p><span className="font-semibold">Symbol:</span> {log.symbol}</p>
                <p><span className="font-semibold">Amount:</span> {log.amount}</p>
                <p><span className="font-semibold">Price:</span> {log.price}</p>
                <p><span className="font-semibold">Timestamp:</span> {log.timestamp}</p>
                <p><span className="font-semibold">Balance After:</span> {log.balance_after}</p>
              </div>
            ))
          )}
        </div>
      </div>
    );
  }
  