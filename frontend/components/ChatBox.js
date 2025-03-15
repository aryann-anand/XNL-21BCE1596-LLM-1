import { useState } from 'react';

export default function ChatBox() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSend = async () => {
    if (query.trim() === "") return;
    // Append user query and send to backend
    const newMessages = [...messages, { sender: "user", text: query }];
    setMessages(newMessages);
    const res = await fetch("http://localhost:8000/api/chat", {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });
    const data = await res.json();
    setMessages([...newMessages, { sender: "bot", text: data.response }]);
    setQuery("");
  };

  return (
    <div className="bg-white p-4 rounded shadow h-full flex flex-col">
      <h2 className="text-xl font-bold mb-4">Customer Query Chat</h2>
      <div className="flex-1 overflow-y-auto mb-4">
        {messages.map((msg, index) => (
          <div key={index} className={`mb-2 ${msg.sender === "user" ? "text-right" : "text-left"}`}>
            <span className={`inline-block p-2 rounded ${msg.sender === "user" ? "bg-blue-500 text-white" : "bg-gray-300 text-black"}`}>
              {msg.text}
            </span>
          </div>
        ))}
      </div>
      <div className="flex">
        <input 
          type="text" 
          className="flex-1 border border-gray-300 rounded p-2"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Type your query..."
        />
        <button onClick={handleSend} className="ml-2 bg-blue-500 text-white p-2 rounded">
          Send
        </button>
      </div>
    </div>
  );
}
