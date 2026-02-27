import { useState } from 'react';

const testData = {
  "Greeting & Basics": [
    {
      name: "user greets the assistant",
      steps: [
        { type: "user", text: "hi" },
        { type: "bot", text: "utter_greeting" }
      ]
    },
    {
      name: "user asks what the bot can do",
      steps: [
        { type: "user", text: "what can you do?" },
        { type: "bot", text: "utter_what_can_you_do" }
      ]
    },
    {
      name: "user asks who the bot is",
      steps: [
        { type: "user", text: "who are you?" },
        { type: "bot", text: "utter_who_are_you" }
      ]
    },
    {
      name: "user says goodbye",
      steps: [
        { type: "user", text: "bye" },
        { type: "bot", text: "utter_goodbye" }
      ]
    },
    {
      name: "user asks for help",
      steps: [
        { type: "user", text: "help" },
        { type: "bot", text: "utter_help" }
      ]
    }
  ],
  "Heating Check": [
    {
      name: "user reports heating not working",
      steps: [
        { type: "user", text: "my heating isn't working" },
        { type: "bot", text: "utter_checking_heating" },
        { type: "bot", text: "utter_heating_on" }
      ]
    },
    {
      name: "user asks to check heating",
      steps: [
        { type: "user", text: "can you check my heating?" },
        { type: "bot", text: "utter_checking_heating" },
        { type: "bot", text: "utter_heating_on" }
      ]
    },
    {
      name: "user asks if thermostat is online",
      steps: [
        { type: "user", text: "is my thermostat online?" },
        { type: "bot", text: "utter_checking_heating" },
        { type: "bot", text: "utter_heating_on" }
      ]
    }
  ],
  "Can't Do": [
    {
      name: "user asks to control smart plugs",
      steps: [
        { type: "user", text: "can you control my smart plugs?" },
        { type: "bot", text: "utter_unsupported_action" }
      ]
    },
    {
      name: "user asks to turn up heating",
      steps: [
        { type: "user", text: "turn my heating up to 23 degrees" },
        { type: "bot", text: "utter_unsupported_action" }
      ]
    }
  ],
  "Emotions": [
    {
      name: "user is rude - handle gracefully",
      steps: [
        { type: "user", text: "you're useless" },
        { type: "bot", text: "utter_insult_response" }
      ]
    },
    {
      name: "user says ok after help",
      steps: [
        { type: "user", text: "check my heating" },
        { type: "bot", text: "utter_checking_heating" },
        { type: "bot", text: "utter_heating_on" },
        { type: "user", text: "ok" },
        { type: "bot", text: "utter_free_chitchat_response" }
      ]
    }
  ],
  "Multi-Turn": [
    {
      name: "new user explores then checks heating",
      steps: [
        { type: "user", text: "hello" },
        { type: "bot", text: "utter_greeting" },
        { type: "user", text: "what can you help me with?" },
        { type: "bot", text: "utter_what_can_you_do" },
        { type: "user", text: "ok can you check my heating" },
        { type: "bot", text: "utter_checking_heating" },
        { type: "bot", text: "utter_heating_on" },
        { type: "user", text: "thanks" },
        { type: "bot", text: "utter_free_chitchat_response" },
        { type: "user", text: "bye" },
        { type: "bot", text: "utter_goodbye" }
      ]
    },
    {
      name: "user gets help then says ok",
      steps: [
        { type: "user", text: "my house is cold" },
        { type: "bot", text: "utter_checking_heating" },
        { type: "bot", text: "utter_heating_on" },
        { type: "user", text: "ok" },
        { type: "bot", text: "utter_free_chitchat_response" }
      ]
    },
    {
      name: "user asks about capabilities then checks heating",
      steps: [
        { type: "user", text: "hi" },
        { type: "bot", text: "utter_greeting" },
        { type: "user", text: "can you turn my heating up?" },
        { type: "bot", text: "utter_unsupported_action" },
        { type: "user", text: "can you at least check if it's working?" },
        { type: "bot", text: "utter_checking_heating" },
        { type: "bot", text: "utter_heating_on" }
      ]
    },
    {
      name: "quick heating check",
      steps: [
        { type: "user", text: "check my thermostat" },
        { type: "bot", text: "utter_checking_heating" },
        { type: "bot", text: "utter_heating_on" },
        { type: "user", text: "great" },
        { type: "bot", text: "utter_free_chitchat_response" }
      ]
    }
  ]
};

function ConversationBubble({ step }) {
  const isUser = step.type === 'user';
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-xs rounded-2xl px-4 py-2 ${
        isUser
          ? 'bg-orange-500 text-white rounded-br-md'
          : 'bg-gray-200 text-gray-800 rounded-bl-md'
      }`}>
        <p className="text-sm">{step.text}</p>
      </div>
    </div>
  );
}

function TestCard({ test, category }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="border-b border-gray-100 px-4 py-3 bg-gray-50">
        <span className="text-xs font-medium text-orange-500 uppercase tracking-wide">{category}</span>
        <h3 className="text-sm font-semibold text-gray-800 mt-0.5">{test.name}</h3>
      </div>
      <div className="p-4 space-y-2 bg-gradient-to-b from-gray-50 to-white">
        {test.steps.map((step, i) => (
          <ConversationBubble key={i} step={step} />
        ))}
      </div>
    </div>
  );
}

export default function TestCaseViewer() {
  const [filter, setFilter] = useState('All');

  const categories = ['All', ...Object.keys(testData)];

  const allTests = [];
  Object.entries(testData).forEach(([category, tests]) => {
    tests.forEach(test => {
      allTests.push({ ...test, category });
    });
  });

  const filteredTests = filter === 'All'
    ? allTests
    : allTests.filter(t => t.category === filter);

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-800 mb-1">Hive Bot Test Cases</h1>
        <p className="text-sm text-gray-500 mb-4">{allTests.length} test conversations</p>

        <div className="flex gap-2 mb-4 flex-wrap">
          {categories.map(cat => (
            <button
              key={cat}
              onClick={() => setFilter(cat)}
              className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
                filter === cat
                  ? 'bg-orange-500 text-white'
                  : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200'
              }`}
            >
              {cat} {cat === 'All' ? `(${allTests.length})` : `(${testData[cat].length})`}
            </button>
          ))}
        </div>

        <div className="space-y-4">
          {filteredTests.map((test, i) => (
            <TestCard key={i} test={test} category={test.category} />
          ))}
        </div>

        <p className="text-xs text-gray-400 mt-6 text-center">
          Bot responses shown as utter_* template names
        </p>
      </div>
    </div>
  );
}
