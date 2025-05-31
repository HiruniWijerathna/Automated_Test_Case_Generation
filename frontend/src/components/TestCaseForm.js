import React, { useState } from 'react';
import axios from 'axios';

const TestCaseForm = () => {
  const [inputType, setInputType] = useState("code");
  const [content, setContent] = useState("");
  const [engine, setEngine] = useState("huggingface");
  const [result, setResult] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
     const response = await axios.post("http://localhost:8000/generate-testcases", {
  input_type: inputType,
  content: content,
  engine: engine
});

      setResult(response.data.test_cases);
    } catch (error) {
      alert("Error generating test cases");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h2>Automated Test Case Generator</h2>
      <form onSubmit={handleSubmit}>
        <label>Input Type:</label>
        <select value={inputType} onChange={(e) => setInputType(e.target.value)}>
          <option value="code">Code</option>
          <option value="requirement">Requirement</option>
        </select>

        <label>AI Engine:</label>
        <select value={engine} onChange={(e) => setEngine(e.target.value)}>
          <option value="huggingface">Hugging Face</option>
          <option value="openai">OpenAI GPT</option>
        </select>

        <label>Input:</label>
        <textarea rows="8" value={content} onChange={(e) => setContent(e.target.value)} />

        <button type="submit" disabled={loading}>
          {loading ? "Generating..." : "Generate Test Cases"}
        </button>
      </form>

      <div className="result">
        <h3>Generated Test Cases</h3>
        <pre>{result && result.join("\n\n")}</pre>
      </div>
    </div>
  );
};

export default TestCaseForm;
